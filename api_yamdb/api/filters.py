from django_filters import FilterSet, filters

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтрация для ресурса titles."""

    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
