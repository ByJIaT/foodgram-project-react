# Generated by Django 4.2.3 on 2023-07-11 10:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Ingredient name')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Measurement unit')),
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
                ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Recipe image')),
                ('text', models.TextField(verbose_name='Recipe description')),
                ('cooking_time', models.IntegerField(help_text='Cooking time in minutes', validators=[django.core.validators.MinValueValidator(1, message='Must be more then 1 minute')], verbose_name='Cooking time')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, help_text='Amount of ingredients', validators=[django.core.validators.MinValueValidator(1, message='Must be more then 1')], verbose_name='Ingredient amount')),
            ],
            options={
                'verbose_name': 'RecipeIngredient',
                'verbose_name_plural': 'RecipeIngredients',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'RecipeTag',
                'verbose_name_plural': 'RecipeTags',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Tag name')),
                ('color', models.CharField(max_length=7, null=True, unique=True, verbose_name='Tag color')),
                ('slug', models.SlugField(max_length=200, null=True, unique=True, verbose_name='Tag slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'indexes': [models.Index(fields=['name'], name='recipes_tag_name_56fd94_idx')],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcarts', to='recipes.recipe', verbose_name='ShoppingCart recipes')),
            ],
            options={
                'verbose_name': 'ShoppingCart',
                'verbose_name_plural': 'ShoppingCarts',
            },
        ),
    ]
