from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class AdminUser(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    exclude = ("password",)
    readonly_fields = ("last_login", "date_joined")
    filter_horizontal = ()
