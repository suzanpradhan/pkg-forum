from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel

from src.user.manager import CustomAccountManager


class User(AbstractBaseUser, SafeDeleteModel, PermissionsMixin):
    """
    Custom Account User: email, first_name, last_name, username, is_staff, phone, address, avatar
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    profile = models.OneToOneField(
        "Profile",
        related_name="user_profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email if self.email is not None else "No Email"

    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        """
        Meta
        """

        ordering = ["created_on"]


class GenderChoices(models.TextChoices):
    """
    Gender Choices
    """

    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")
    UNKNOWN = "UNKNOWN", _("Unknown")


def get_upload_path_for_avatar(instance, filename):
    """
    Custom Upload Path for User Avatar
    """
    return f"avatars/users/{instance.id}/{filename}"


class Profile(models.Model):
    """
    User Profile
    """

    full_name = models.CharField(_("full name"), max_length=255, blank=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    secondary_email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GenderChoices.choices, null=True)
    birth_date = models.DateField(null=True)
    avatar = models.ImageField(
        upload_to=get_upload_path_for_avatar, null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
