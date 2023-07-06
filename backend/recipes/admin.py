from django.contrib import admin

from recipes.models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart,
)


class IngredientsRecipeInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsRecipeInline,)
    list_display = (
        'author', 'get_tags', 'name', 'get_ingredients', 'image', 'text',
        'cooking_time',
    )
    fields = ()
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-empty-'

    @admin.display(description='ingredients')
    def get_ingredients(self, obj):
        return '\n'.join([ingredient.name for ingredient in
                          obj.ingredients.all()])

    @admin.display(description='tags')
    def get_tags(self, obj):
        return '\n'.join([tag.name for tag in obj.tags.all()])


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-empty-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-empty-'
