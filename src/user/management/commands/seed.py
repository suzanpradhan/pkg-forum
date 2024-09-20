from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from src.user.models import User

MODE_REFRESH = "refresh"
MODE_CLEAR = "clear"


class Command(BaseCommand):
    """
    Seeder Command
    """

    help = "Seeder Command"

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        run_seed(self, options["mode"])


def clear_data():
    """Deletes all the Roles data"""
    Group.objects.all().delete()


def create_roles():
    """
    Seed Default Roles
    """
    group = Group.objects.create(name="Admin")
    group.permissions.add(*Permission.objects.all())
    admin_user_query = User.objects.filter(username="admin")
    if admin_user_query.exists():
        admin_user = admin_user_query.first()
        admin_user.groups.add(group)


def run_seed(self, mode):
    """Seed database based on mode"""

    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    create_roles()
