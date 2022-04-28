from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitlesViewSet, UserViewSet,
                       get_confirmation_number, get_token)

app_name = 'api'


v1_router = DefaultRouter()
v1_router.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)
v1_router.register(
    'genres',
    GenresViewSet,
    basename='genres'
)
v1_router.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='coomments'
)
v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/auth/signup/', get_confirmation_number, name='signup'),
]
