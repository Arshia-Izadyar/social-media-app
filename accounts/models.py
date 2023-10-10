from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers import CustomUserManager
class User(AbstractUser):
    BLUE_USER = 1
    FREE_USER = 0
    OFFICIAL_USER = 2
    
    user_type = (
        (BLUE_USER, "blueUser"),
        (FREE_USER, "freeUser"),
        (OFFICIAL_USER, "officialUser"),
    )
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")
    email = models.EmailField(verbose_name=_("Email"), max_length=200, unique=True)
    # TODO: add phone validator
    phone_number = models.CharField(verbose_name=_("Phone number"), max_length=14, unique=True)
    is_admin = models.BooleanField(default=False, verbose_name=_("Is admin"))
    user_type = models.PositiveSmallIntegerField(verbose_name=_("user type"), choices=user_type, default=FREE_USER)
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff"))
    is_active = models.BooleanField(verbose_name=_("Active"),default=False)
    # TODO: add validator and default username generator
    username = models.CharField(max_length=200, unique=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True) 
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("phone_number", "email")
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def is_following(self, user):
        return self.followers.filter(pk=user.pk).exists()
    
