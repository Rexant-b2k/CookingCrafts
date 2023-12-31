# flake8: noqa
# Generated by Django 4.2.5 on 2023-10-08 04:29

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Favourite',
                'verbose_name_plural': 'Favourites',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Ingredient name')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Ingredient measurement unit')),
            ],
            options={
                'verbose_name': 'Ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Amount of ingredients')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Recipe name')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Recipe image')),
                ('description', models.TextField(verbose_name='Full description of recipe')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32000)], verbose_name='Cooking time in minutes')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name for the tag, max 200 characters', max_length=200, unique=True, verbose_name='Tag Name')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, unique=True, verbose_name='Tag color in HEX format')),
                ('slug', models.SlugField(max_length=200, unique=True, validators=[recipes.validators.TagSlugValidator], verbose_name='Tag slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_%(class)s', to='recipes.recipe', verbose_name='%(class) recipe')),
            ],
            options={
                'verbose_name': 'Shopping list',
                'verbose_name_plural': 'Shopping lists',
                'abstract': False,
            },
        ),
    ]
