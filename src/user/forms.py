from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Account Create Form
    """

    class Meta(UserCreationForm):
        """
        Meta
        """

        model = User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    """
    Account Change Form
    """

    class Meta(UserChangeForm):
        """
        Meta
        """

        model = User
        fields = ("email", "username")
