from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.Serializer):
    """Сериализатор для метода get_confirmation_number."""

    password = None
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(
                'Вы не можете использовать это имя пользователя.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для метода get_token."""

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    def validate_confirmation_code(self, value):
        if value == '':
            raise ValidationError('Это поле не может быть пустым.')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета UserViewSet."""

    class Meta:
        model = User
        fields = (
            'username',
            'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета UserViewSet ресурса users/me."""

    class Meta:
        model = User
        fields = (
            'username',
            'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета CategoriesViewSet."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета GenresViewSet."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ReadTitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета TitlesViewSet (чтение)."""

    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class WriteTitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета TitlesViewSet (запись)."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category'
        )

    def validate_year(self, value):
        """Проверка поля поля year на реалистичность."""

        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше настоящего'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета ReviewViewSet."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Можно оставить только один отзыв на произведение.'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для вьюсета CommentViewSet."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
