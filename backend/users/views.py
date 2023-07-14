from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.mixins import DeleteMixin, CreateMixin
from core.pagination import LimitPageNumberPagination
from users.models import Subscription
from users.serializers.subscription_serializer import SubscriptionSerializer

User = get_user_model()


class CustomUserViewSet(CreateMixin, DeleteMixin, UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(('post',), detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        fields = {
            'user': request.user,
            'author': get_object_or_404(User, pk=id),
        }
        if fields['user'] == fields['author']:
            return Response(
                {'errors': _('Self subscription not possible')},
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.created(model=Subscription,
                            serializer=SubscriptionSerializer,
                            instance=fields['author'],
                            context=self.get_serializer_context(),
                            error_message='You are already subscribed',
                            **fields,
                            )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        fields = {
            'user': request.user,
            'author': get_object_or_404(User, pk=id),
        }
        return self.deleted(model=Subscription,
                            error_message='You are not subscribed',
                            **fields,
                            )

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        subscriptions = User.objects.filter(subscriptions__user=request.user)

        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscriptionSerializer(
                page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(
            subscriptions, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status.HTTP_200_OK)
