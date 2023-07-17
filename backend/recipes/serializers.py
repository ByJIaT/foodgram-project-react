from django.db.models import F
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.fields import Base64ImageField
from core.mixins import CreateUpdateNestedMixin
from core.utils import is_digit
from recipes.models import (Tag, Ingredient, Recipe)
from users.serializers.user_serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeMiniFieldSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class BaseRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.favorites.is_favorited(
            self.context.get('request').user,
            recipe,
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.shopping_carts.is_in_shopping_cart(
            self.context.get('request').user,
            recipe,
        )


class RecipeReadOnlySerializer(BaseRecipeSerializer):
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, recipe):
        return recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F(
                'recipe_ingredients__amount')
        )


class RecipeSerializer(CreateUpdateNestedMixin, BaseRecipeSerializer):

    def validate(self, attrs):
        ingredients_id = [
            ingredient['id'] for ingredient in attrs['ingredients']]

        if len(ingredients_id) != len(set(ingredients_id)):
            raise serializers.ValidationError(_('Duplicate ingredients'))

        for ingredient in attrs['ingredients']:
            if not is_digit(ingredient['amount']):
                raise serializers.ValidationError(
                    _('Enter a number in the weight of the ingredient'))

            if int(ingredient['amount']) < 1:
                raise serializers.ValidationError(
                    _('Ingredients must be greate then 0'))

        return attrs

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['ingredients'] = data['ingredients']
        return result

    def to_representation(self, instance):
        return RecipeReadOnlySerializer(
            instance,
            context=self.context,
        ).data
