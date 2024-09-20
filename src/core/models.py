from django.contrib.auth import get_user_model
from django.db import models
from safedelete.config import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel
from safedelete.queryset import SafeDeleteQueryset

from src.core.managers import ZenBaseManager


class AccessSupport(models.Model):
    """
    Access Support Model
    """

    class Meta:
        """
        Meta
        """

        managed = False

        default_permissions = ()

        permissions = ()


class ZenBaseModel(SafeDeleteModel):
    """
    Custom Base Model: [created_on, modified_on, created_by, modified_by]
    """

    _safedelete_policy: int = SOFT_DELETE_CASCADE

    zenQueryset = SafeDeleteQueryset

    objects = ZenBaseManager.from_queryset(zenQueryset)()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        related_name="%(class)s_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        related_name="%(class)s_modified_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta Class"""

        abstract = True
