from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from cookingcrafts.constants import Recipe as R

from .validators import TagSlugValidator


class Tag(models.Model):
    name = models.CharField(
        _('Tag Name'),
        max_length=R.MAX_TAG_NAME,
        help_text=_('Name for the tag, max 200 characters'),
        unique=True,
        blank=False,
    )
    color = ColorField(
        _('Tag color in HEX format'),
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        _('Tag slug'),
        max_length=R.MAX_TAG_SLUG,
        validators=(TagSlugValidator,),
        unique=True,
        blank=False,
    )

    def __str__(self) -> str:
        return f'{self.name} (slug: {self.slug})'

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Ingredient(models.Model):
    name = models.CharField(
        _('Ingredient name'),
        max_length=R.MAX_INGREDIENT_NAME,
        blank=False,
    )
    measurement_unit = models.CharField(
        _('Ingredient measurement unit'),
        max_length=R.MAX_INGREDIENT_M_UNIT,
        blank=False,
    )

    def __str__(self) -> str:
        return f'{self.name} ({self.measurement_unit})'

    class Meta:
        ordering = ['name']
        verbose_name = _('Ingredient')
        verbose_name = _('Ingredients')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_Ingredient_entry'
            )
        ]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author',
        blank=False,
    )
    name = models.CharField(
        _('Recipe name'),
        max_length=R.MAX_RECIPE_NAME,
        blank=False,
    )
    image = models.ImageField(
        _('Recipe image'),
        upload_to='recipes/',
        blank=False
    )
    description = models.TextField(
        _('Full description of recipe'),
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='ingredients',
        verbose_name=_('Ingredients'),
        blank=False,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name=_('Recipe tags'),
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        _('Cooking time in minutes'),
        validators=(MinValueValidator(R.MIN_COOKING_TIME),
                    MaxValueValidator(R.MAX_COOKING_TIME)),
        blank=False,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipes',
        verbose_name=_('Ingredient name'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    amount = models.PositiveSmallIntegerField(
        _('Amount of ingredients'),
        blank=False,
        validators=(MinValueValidator(R.MIN_INGR_AMOUNT),),
    )

    def __str__(self) -> str:
        return f'{self.ingredient} in {self.recipe}'

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')


class UserRecipeAModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name=_('User'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_%(class)s',
        verbose_name=_('%(class) recipe'),
    )

    def __str__(self) -> str:
        return f'{self.user} - {self.recipe}'

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_%(class)s_entry'
            )
        ]


class Favourite(UserRecipeAModel):

    class Meta(UserRecipeAModel.Meta):
        verbose_name = _('Favourite')
        verbose_name_plural = _('Favourites')


class ShoppingList(UserRecipeAModel):

    class Meta(UserRecipeAModel.Meta):
        verbose_name = _('Shopping list')
        verbose_name_plural = _('Shopping lists')
