from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Get a list of all permissions available in the system
    """

    help = "Get a list of all permissions available in the system"

    def handle(self, *args, **options):
        print(ContentType.objects.all())
        permissions = set()
        # We create (but not persist) a temporary superuser and use it to game the
        # system and pull all permissions easily.
        tmp_superuser = get_user_model()(is_superuser=True)
        for backend in auth.get_backends():
            if hasattr(backend, "get_all_permissions"):
                permissions.update(backend.get_all_permissions(tmp_superuser))

        # Output unique list of permissions sorted by permission name.
        sorted_list_of_permissions = sorted(list(permissions))
        self.stdout.write("\n".join(sorted_list_of_permissions))
