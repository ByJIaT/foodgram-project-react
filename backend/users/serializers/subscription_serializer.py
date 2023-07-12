from rest_framework import serializers

from recipes.serializers import RecipeMiniFieldSerializer
from users.serializers.user_serializers import CustomUserSerializer


class SubscriptionSerializer(CustomUserSerializer):
    recipes = RecipeMiniFieldSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_recipes_count(self, user):
        return user.recipes.count()
