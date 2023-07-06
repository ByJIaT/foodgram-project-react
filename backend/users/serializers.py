from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user == obj or user.is_anonymous:
            return False
        return user.users_subscription_user.is_subscribed(
            user, obj)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password'
        )


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = ('__all__',)

    @staticmethod
    def get_recipes(obj):
        return obj.recipes_recipe.get_recipes()

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes_recipe.get_recipes_count()
