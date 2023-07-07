from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Subscription
from users.serializers import SubscriptionSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(('post',), detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        if Subscription.objects.is_subscribed(user, author):
            return Response(
                {'errors': _('Self subscription not possible')},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user == author:
            return Response(
                {'errors': _('You are already subscribed')},
                status=status.HTTP_400_BAD_REQUEST
            )

        Subscription.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(author)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        if not Subscription.objects.is_subscribed(user, author):
            return Response(
                {'errors': _('You are not subscribed')},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.delete(user, author)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        pages = self.paginate_queryset(
            User.objects.filter(users_subscription_author__user=request.user)
        )
        serializer = SubscriptionSerializer(
            pages,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
