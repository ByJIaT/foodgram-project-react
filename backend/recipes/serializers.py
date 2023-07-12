import collections

from django.db.models import F
from rest_framework import serializers

from core.fields import Base64ImageField
from core.mixins import CreateUpdateNestedMixin
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
        return recipe.shoppingcarts.is_in_shopping_cart(
            self.context.get('request').user,
            recipe,
        )


class RecipeReadOnlySerializer(BaseRecipeSerializer):
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, recipe):
        return recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )


class RecipeSerializer(CreateUpdateNestedMixin, BaseRecipeSerializer):

    def validate(self, attrs):
        ingredients = self.initial_data['ingredients']
        ingredients_id = collections.Counter(
            [ingredient['id'] for ingredient in ingredients])

        if any(map(lambda value: value > 1, ingredients_id.values())):
            raise serializers.ValidationError('Duplicate ingredients')

        return attrs

    def to_representation(self, instance):
        return RecipeReadOnlySerializer(
            instance,
            context=self.context,
        ).data
