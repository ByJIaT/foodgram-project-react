from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, )
    last_name = models.CharField(_('last name'), max_length=150, )

    REQUIRED_FIELDS = ['email', 'last_name', 'first_name', ]

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_email_username',
            )
        ]
        indexes = [
            models.Index(fields=('username',)),
        ]
