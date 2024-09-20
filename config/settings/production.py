# pylint: disable=missing-module-docstring
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from config.settings.base import *

DEBUG = True

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
    }
}
