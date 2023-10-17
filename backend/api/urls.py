from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet, 'tags')
router.register(r'ingredients', views.IngredientViewSet, 'ingredients')
router.register(r'recipes', views.RecipeViewSet, 'recipes')

urlpatterns = [
    path('', include(router.urls)),
]
