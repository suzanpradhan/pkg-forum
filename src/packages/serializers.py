from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Package, Registry, PackageSocial
from src.core.fields import ZenModelSerializeIntegerField


class RegistrySerializer(serializers.ModelSerializer):
    """ "
    Serializer for Registry
    """

    class Meta:
        """
        Meta Class
        """

        model = Registry
        fields = "__all__"


class PackageSocialSerializer(serializers.ModelSerializer):
    """ "
    Serializer for Package Social
    """

    class Meta:
        """
        Meta Class
        """

        model = PackageSocial
        fields = "__all__"


class PackageSerializer(WritableNestedModelSerializer):
    """ "
    Serializer for Package
    """

    registry = ZenModelSerializeIntegerField(
        model=Registry, serializer=RegistrySerializer
    )
    socials = PackageSocialSerializer(many=True)

    class Meta:
        """
        Meta Class
        """

        model = Package
        fields = "__all__"
