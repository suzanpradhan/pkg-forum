from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from src.user.services.account_service import generate_random_password


class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.save()
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("You must provide an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        if password is None:
            password = generate_random_password(32)

        user.set_password(password)
        user.save()
        return user

    def get_or_create_user(self, email, **defaults):
        """
        Get or Create Account
        """
        try:
            user, created = self.get(email=email), False
        except self.model.DoesNotExist:
            user, created = self.create_user(email, **defaults), True
        return user, created
