from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core import exceptions


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise exceptions.ValidationError("users must have email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise exceptions.ImproperlyConfigured(_("Super user must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise exceptions.ImproperlyConfigured(_("Super User must have is_superuser=True"))
        return self.create_user(email, password, **extra_fields)
