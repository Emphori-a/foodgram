from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, IngredientViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),

]
