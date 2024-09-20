from functools import partial

from rest_framework.response import Response


class FieldPermissionSerializerMixin:
    """
    ModelSerializer logic for marking fields as ``read_only=True`` when a user is found not to have
    change permissions.
    """

    REQUEST_METHODS = ["POST", "PUT", "PATCH"]

    def __init__(self, *args, **kwargs):
        super(FieldPermissionSerializerMixin, self).__init__(*args, **kwargs)

        if self.context["request"] in self.REQUEST_METHODS:
            user = self.context["request"].user
            model = self.Meta.model
            model_field_names = [
                f.name for f in model._meta.get_fields()
            ]  # this might be too broad
            for name in model_field_names:
                if name in self.fields and not self.instance.has_field_perm(
                    user, field=name
                ):
                    self.fields[name].read_only = True


class FieldPermissionModelMixin:
    """
    Mixin for Field Level Permission
    """

    field_permissions = {}  # {'field_name': callable}
    FIELD_PERM_CODENAME = "can_change_{model}_{name}"
    FIELD_PERMISSION_GETTER = "can_change_{name}"
    FIELD_PERMISSION_MISSING_DEFAULT = True

    class Meta:
        """
        Meta Class
        """

        abstract = True

    def has_perm(self, user, perm):
        """
        Check for User Permission
        # Never give 'obj' argument here
        """
        return user.has_perm(perm)

    def has_field_perm(self, user, field):
        """
        Check for each field permission
        """
        if field in self.field_permissions:
            checks = self.field_permissions[field]
            if not isinstance(checks, (list, tuple)):
                checks = [checks]
            for i, perm in enumerate(checks):
                if callable(perm):
                    checks[i] = partial(perm, field=field)

        else:
            checks = []

            # Consult the optional field-specific hook.
            getter_name = self.FIELD_PERMISSION_GETTER.format(name=field)
            if hasattr(self, getter_name):
                checks.append(getattr(self, getter_name))

            # Try to find a static permission for the field
            else:
                perm_label = self.FIELD_PERM_CODENAME.format(
                    **{
                        "model": self._meta.model_name,
                        "name": field,
                    }
                )
                if perm_label in dict(self._meta.permissions):
                    checks.append(self._meta.model_name + "." + perm_label)

        # No requirements means no restrictions.
        if not checks:
            return self.FIELD_PERMISSION_MISSING_DEFAULT

        # Try to find a user setting that qualifies them for permission.
        for perm in checks:
            if callable(perm):
                result = perm(self, user=user)
                if result is not None:
                    return result

            else:
                result = user.has_perm(
                    perm
                )  # Don't supply 'obj', or else infinite recursion.
                if result:
                    return True

        # If no requirement can be met, then permission is denied.
        return False


class ZenListModelMixin:
    """
    List Model Mixin.
    """

    # pylint: disable=unused-argument
    def list(self, request, *args, **kwargs):
        """
        List a queryset.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, *args, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, *args, **kwargs)
        return Response(serializer.data)


class PermissionPolicyMixin:
    """
    Setup Permissions based on request methods
    """

    def check_permissions(self, request):
        """
        Checks Permissions
        """
        try:
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(
                handler.__name__
            )

        super().check_permissions(request)
