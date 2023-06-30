from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_superuser', 'is_staff', 'is_active',
    )
    search_fields = ('username',)
    list_filter = ('email', 'username',)
    empty_value_display = '-empty-'
