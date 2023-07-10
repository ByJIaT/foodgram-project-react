from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, )
    last_name = models.CharField(_('last name'), max_length=150, )

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='%(app_label)s_%(class)s',
            )
        ]
        indexes = [
            models.Index(fields=('username',)),
        ]


class SubscriptionManager(models.Manager):
    def is_subscribed(self, user, author):
        return self.filter(user=user, author=author).exists()

    def delete(self, user, author):
        return self.filter(user=user, author=author).delete()


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription_users',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription_authors',
    )

    objects = SubscriptionManager()

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='%(app_label)s_%(class)s',
            )
        ]
        indexes = [
            models.Index(fields=('user',))
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
