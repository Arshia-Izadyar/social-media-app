from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("username", "email", "is_staff", "is_active", "phone_number")
    list_filter = (
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "user_type","last_name","first_name", "birth_day", "location", "bio")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone_number", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

