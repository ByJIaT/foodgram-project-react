from django_filters.rest_framework import (
    FilterSet, CharFilter, AllValuesMultipleFilter, BooleanFilter)

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(method='get_filters_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_filters_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ()

    def get_filters_is_favorited(self, queryset, name, value):
        if not value and self.request.user.is_anonymous:
            return queryset
        return queryset.filter(favorites__user=self.request.user)

    def get_filters_is_in_shopping_cart(self, queryset, name, value):
        if not value and self.request.user.is_anonymous:
            return queryset
        return queryset.filter(shopping_carts__user=self.request.user)
