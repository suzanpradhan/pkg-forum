from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField, IntegerField

from .serializers import DynamicFieldsModelSerializer


class ModelIdField(IntegerField):
    """
    Serializer Field for Model id field
    """

    def __init__(self, model_field: Model, **kwargs):
        self.model_field = model_field
        kwargs["error_messages"] = {
            "model_invalid": _(f"Can't find {model_field.__name__} of given id.")
        }
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not self.model_field.objects.filter(id=data).exists():
            self.fail("model_invalid")
        return super().to_internal_value(data)

    def to_representation(self, value):
        return self.model_field.objects.filter(id=int(value)).first()


class ZenModelSerializeIntegerField(IntegerField):
    """
    Zen[Model+Serializer]IntegerField

    Model object on write, Serialized data or Primary key on read

    Default filtered by "id", can be customized with param: filterBy
    """

    def __init__(
        self,
        model: Model,
        serializer=None,
        filter_by="id",
        required=False,  # Required is set to False as default
        allow_null=False,  # Required is set to False as default
        **kwargs,
    ):
        self.model = model
        self.serializer = serializer
        self.filter_by = filter_by
        self.fields = kwargs.pop("fields", None)
        self.exclude_fields = kwargs.pop("exclude_fields", None)
        kwargs["error_messages"] = {
            "model_invalid": _(f"Can't find {model.__name__} of given id.")
        }
        kwargs["required"] = required
        kwargs["allow_null"] = allow_null
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not self.model.objects.filter(
            **{f"{self.filter_by}__iexact": data}
        ).exists():
            self.fail("model_invalid")
        data = super().to_internal_value(data)
        return self.model.objects.filter(**{f"{self.filter_by}__iexact": data}).first()

    def to_representation(self, value):
        if not self.serializer:
            return value.pk
        kwargs = {}
        if self.fields:
            kwargs["fields"]: self.fields
        if self.exclude_fields:
            kwargs["exclude_fields"]: self.exclude_fields
        return self.serializer(value, **kwargs).data


class ZenModelSerializeCharField(CharField):
    """
    Zen[Model+Serializer]IntegerField

    Model object on write, Serialized data or Primary key on read

    Default filtered by "id", can be customized with param: filterBy
    """

    def __init__(
        self,
        model: Model,
        serializer=None,
        filter_by="id",
        required=False,  # Required is set to False as default
        **kwargs,
    ):
        self.model = model
        self.serializer = serializer
        self.filter_by = filter_by
        self.fields = kwargs.pop("fields", None)
        self.exclude_fields = kwargs.pop("exclude_fields", None)
        kwargs["error_messages"] = {
            "model_invalid": _(f"Can't find {model.__name__} of given id.")
        }
        kwargs["required"] = required
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not self.model.objects.filter(
            **{f"{self.filter_by}__icontains": data}
        ).exists():
            self.fail("model_invalid")
        data = super().to_internal_value(data)
        return self.model.objects.filter(
            **{f"{self.filter_by}__icontains": data}
        ).first()

    def to_representation(self, value):
        if not self.serializer:
            return value.pk
        kwargs = {}
        if self.fields:
            kwargs["fields"] = self.fields
        if self.exclude_fields:
            kwargs["exclude_fields"] = self.exclude_fields
        return self.serializer(value, **kwargs).data
