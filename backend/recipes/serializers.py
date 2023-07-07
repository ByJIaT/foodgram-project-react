import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from core.mixins import CreateUpdateNestedMixin
from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredient)
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class RecipeSerializer(CreateUpdateNestedMixin, serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        recipe_id = representation['id']
        for ingredient in representation['ingredients']:
            amount = RecipeIngredient.objects.get(
                recipe_id=recipe_id, ingredient_id=ingredient['id']).amount
            ingredient.update({'amount': amount})
        return representation

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.favorite_recipes.is_favorited(
            self.context.get('request').user,
            recipe,
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.shoppingcart_recipes.is_in_shopping_cart(
            self.context.get('request').user,
            recipe,
        )
