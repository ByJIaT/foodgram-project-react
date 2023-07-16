from django_filters.rest_framework import (
    FilterSet, CharFilter, BooleanFilter,
    ModelMultipleChoiceFilter
)

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = BooleanFilter(method='get_filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_filter_is_favorited(self, queryset, name, value):
        if not value and self.request.user.is_anonymous:
            return queryset
        return queryset.filter(favorites__user=self.request.user)

    def get_filter_is_in_shopping_cart(self, queryset, name, value):
        if not value and self.request.user.is_anonymous:
            return queryset
        return queryset.filter(shopping_carts__user=self.request.user)
