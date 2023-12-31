# Generated by Django 4.2.3 on 2023-07-11 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcarts', to=settings.AUTH_USER_MODEL, verbose_name='ShoppingCart users'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='recipes.recipe', verbose_name='Recipes'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='recipes.tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.ingredient', verbose_name='Ingredients'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.recipe', verbose_name='Recipes'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Recipe author'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipeIngredient', to='recipes.ingredient', verbose_name='Recipe ingredients'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipeTag', to='recipes.tag', verbose_name='Recipe tags'),
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='recipes_ing_name_164c6a_idx'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Favorite recipes'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Favorite users'),
        ),
        migrations.AddIndex(
            model_name='shoppingcart',
            index=models.Index(fields=['user'], name='recipes_sho_user_id_c341c5_idx'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='recipes_shoppingcart_recipe_user_uniq'),
        ),
        migrations.AddConstraint(
            model_name='recipetag',
            constraint=models.UniqueConstraint(fields=('recipe', 'tag'), name='recipes_recipetag_recipe_tag_uniq'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipes_recipeingredient_recipe_ingredient_uniq'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['name'], name='recipes_rec_name_891f25_idx'),
        ),
        migrations.AddIndex(
            model_name='favorite',
            index=models.Index(fields=['user'], name='recipes_fav_user_id_2674ef_idx'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='recipes_favorite_recipe_user_uniq'),
        ),
    ]
