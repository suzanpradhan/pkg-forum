from django.db import models
from django.utils.translation import gettext_lazy as _


class Registry(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="registry/", null=True, blank=True)


class Social(models.TextChoices):
    """
    Social Choices
    """

    GITHUB = "github", _("Github")
    WEBSITE = "website", _("Website")
    GITLAB = "gitlab", _("GitLab")
    FAILED = "failed", _("Failed")


class PackageSocial(models.Model):
    link = models.TextField(null=True, blank=True)
    social = models.CharField(
        max_length=20,
        choices=Social.choices,
        default=Social.WEBSITE,
    )


class Package(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    registry = models.ForeignKey(Registry, on_delete=models.SET_NULL, null=True)
    version = models.CharField(max_length=100)
    socials = models.ManyToManyField(PackageSocial)
    image = models.ImageField(upload_to="package_images/", null=True, blank=True)
    cover_image = models.ImageField(upload_to="cover_images/", null=True, blank=True)
