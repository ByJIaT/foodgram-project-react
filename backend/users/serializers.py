from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user == obj:
            return False
        return request_user.users_subscription_user.is_subscribed(
            request_user, obj)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password'
        )

