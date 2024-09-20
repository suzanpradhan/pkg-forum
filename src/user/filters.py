from django_filters import FilterSet

from src.user.models import User


class UserFilter(FilterSet):
    """
    FilterSet For User Model
    """

    class Meta:
        """
        Meta class for User Filter
        """

        model = User
        fields = ["is_staff"]
