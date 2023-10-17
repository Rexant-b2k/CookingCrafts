import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import ValidationError

from cookingcrafts.constants import Recipe as R
from recipes.models import (Favourite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingList, Tag)
from users.serializers import CustomUserSerializer

from .commomserializers import ShortRecipeSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        read_only_fields = ('name',)


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def validate_id(self, value):
        if not Ingredient.objects.filter(id=value).exists():
            raise ValidationError("Ingredient doesn't exists")
        return value

    def validate_amount(self, value):
        if value < R.MIN_INGR_AMOUNT:
            raise ValidationError("Ingredient amount couldn't be less than "
                                  f"{R.MIN_INGR_AMOUNT}")
        return value


class RecipeIngredientRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='description')
    author = CustomUserSerializer()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'author', 'name', 'image', 'ingredients', 'text',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')
        model = Recipe
        read_only_fields = ('__all__',)

    def get_ingredients(self, obj):
        recipe_ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return RecipeIngredientRetrieveSerializer(
            recipe_ingredients, many=True
        ).data

    def get_is_favorited(self, obj):
        return Favourite.objects.filter(
            user=self.context['request'].user.id,
            recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=self.context['request'].user.id,
            recipe=obj).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='description')
    author = CustomUserSerializer(read_only=True,)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    cooking_time = serializers.IntegerField(required=True,
                                            min_value=R.MIN_COOKING_TIME,
                                            max_value=R.MAX_COOKING_TIME)
    image = Base64ImageField(required=True, allow_null=False)
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        fields = ('author', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')
        model = Recipe
        read_only_fields = ('author',)

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError('No ingredients ')
        ingredients_ids = [ingredient['id'] for ingredient in value]
        if len(ingredients_ids) != len(set(ingredients_ids)):
            raise ValidationError('Ingredients should be unique')
        return value

    def validate_tags(self, value):
        if not value:
            raise ValidationError('Shoud be used at least one tag')
        if len(value) != len(set(value)):
            raise ValidationError('Tags should be unique')
        return value

    def validate_image(self, value):
        if not value:
            raise ValidationError('The image is not provided')
        return value

    @staticmethod
    def add_ingredients(recipe, ingredients):
        ingredients_array = []
        for ingredient in ingredients:
            ingredients_array.append(IngredientRecipe(
                ingredient_id=ingredient['id'],
                recipe_id=recipe.id,
                amount=ingredient['amount']))
        return IngredientRecipe.objects.bulk_create(ingredients_array)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.ingredients.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        self.add_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeListRetrieveSerializer(
            instance=instance, context=context
        ).data


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data.get('user').id
        recipe = data.get('recipe')
        if Favourite.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                'The recipe is already in your favourites'
            )
        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        recipe = validated_data.get('recipe')
        return Favourite.objects.create(user=user, recipe=recipe)

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance=instance.recipe).data


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data.get('user').id
        recipe = data.get('recipe')
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                'The recipe is already in your Shopping list'
            )
        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        recipe = validated_data.get('recipe')
        return ShoppingList.objects.create(user=user, recipe=recipe)

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance=instance.recipe).data
