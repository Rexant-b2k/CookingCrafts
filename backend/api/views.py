from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from api import pagintation, serializers
from api.filters import IngredientNameFilter, RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from recipes import models


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
    filter_backends = (IngredientNameFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    pagination_class = pagintation.CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.RecipeListRetrieveSerializer
        return serializers.RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        """
        Because Frontend requires only full update, but
        uses PATCH method
        """
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)

    @action(['post'], detail=True,
            permission_classes=(IsAuthenticated,),)
    def favorite(self, request, pk):
        user = request.user
        if not models.Recipe.objects.filter(id=pk).exists():
            return Response({'detail': 'Not Found'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = models.Recipe.objects.get(id=pk)
        serializer = serializers.FavouriteSerializer(
            context={'request': request},
            data={'user': user.id, 'recipe': recipe.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=pk)
        if models.Recipe.objects.filter(id=pk).exists():
            if not models.Favourite.objects.filter(
                user=user.id, recipe=recipe.id
            ).exists():
                return Response({"detail': The recipe doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        favourite_instance = get_object_or_404(
            models.Favourite, user=user.id, recipe=recipe.id)
        favourite_instance.delete()
        return Response({'detail': 'The recipe was removed from favourites'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=True,
            url_path=r'shopping_cart',
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        user = request.user
        if not models.Recipe.objects.filter(id=pk).exists():
            return Response({'detail': 'Not Found'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = models.Recipe.objects.get(id=pk)
        serializer = serializers.ShoppingListSerializer(
            context={'request': request},
            data={'user': user.id, 'recipe': recipe.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=pk)
        if models.Recipe.objects.filter(id=pk).exists():
            if not models.ShoppingList.objects.filter(
                user=user.id, recipe=recipe.id
            ).exists():
                return Response({"detail': The recipe doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        recipe_in_shopping_list = get_object_or_404(
            models.ShoppingList, user=user.id, recipe=recipe.id
        )
        recipe_in_shopping_list.delete()
        return Response({'detail': 'The recipe was removed from List'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(['get'], detail=False,
            url_path=r'download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = models.IngredientRecipe.objects.filter(
            recipe__users_shoppinglist__user=request.user).values(
                'ingredient__name', 'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(
            ingredient_total=Sum('amount'))
        shopping_list = ['Products to buy to cook selected dishes:\n\n']
        for item in ingredients:
            shopping_list.append(f"{item['ingredient__name']} - "
                                 f"{item['ingredient_total']} "
                                 f"{item['ingredient__measurement_unit']}\n")

        filename = f'{request.user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
