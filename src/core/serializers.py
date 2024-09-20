from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude_fields = kwargs.pop("exclude_fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields is not None:
            excluding = set(exclude_fields)
            for field_name in excluding:
                if field_name in self.fields:
                    self.fields.pop(field_name)


class RelatedFieldMapSerializer(serializers.PrimaryKeyRelatedField):
    """
    Serializer for customizing related field
    """

    def __init__(self, **kwargs):
        self.serializer = kwargs.pop("serializer", None)
        if self.serializer is not None and not issubclass(
            self.serializer, serializers.Serializer
        ):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return not self.serializer

    def to_representation(self, value):
        if self.serializer:
            return self.serializer(value, context=self.context).data
        return super().to_representation(value)


class PermissionSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for Permission
    """

    class Meta:
        """
        Meta Class
        """

        model = Permission
        fields = "__all__"


class GroupSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for Group
    """

    class Meta:
        """
        Meta Class
        """

        model = Group
        fields = "__all__"


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for Content Type
    """

    permissions = serializers.SerializerMethodField()

    class Meta:
        """
        Meta Class
        """

        model = ContentType
        fields = "__all__"

    def get_permissions(self, instance: ContentType):
        """
        Get Content Type Permission
        """
        serializer = PermissionSerializer(
            Permission.objects.filter(content_type=instance).all(),
            fields=("id", "codename"),
            many=True,
        )
        return serializer.data
