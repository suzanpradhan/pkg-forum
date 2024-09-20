# pylint: disable=missing-module-docstring
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from config.settings.base import *

DEBUG = True

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
