import copy

from django.contrib.auth.models import Group, Permission
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from src.core.fields import ModelIdField
from src.user.models import Profile, User


class PermissionListSerializer(serializers.Serializer):
    """
    Serializer for Permission List
    """

    user = ModelIdField(model_field=User)
    group = ModelIdField(model_field=Group)


class UserPermissionSerializer(serializers.Serializer):
    """
    Serializer for User Permission
    """

    user = ModelIdField(model_field=User)


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for Password Reset Request
    """

    email = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for Password Reset
    """

    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError("Passwords should match")
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile
    """

    class Meta:
        """
        Meta Class
        """

        model = Profile
        fields = "__all__"


class UserSerializer(WritableNestedModelSerializer):
    """
    Common Serializer for User
    """

    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()

    class Meta:
        """
        Meta Class
        """

        model = User
        fields = (
            "id",
            "email",
            "is_staff",
            "profile",
            "password",
        )

    def create(self, validated_data: dict):
        profile = None
        if "profile" in validated_data:
            profile = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        if profile:
            user.profile = Profile.objects.create(**profile)
            user.save()
        return user

    def update(self, instance: User, validated_data: dict):
        profile = None
        if "profile" in validated_data:
            profile = validated_data.pop("profile")
        if instance.profile:
            serializer = ProfileSerializer(instance.profile, data=profile, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            instance.profile = Profile.objects.create(**profile)
            instance.save()
        return instance


class UserShortProfileSerializer(UserSerializer):
    """
    Serializer for user short profile
    """

    class Meta:
        """
        Meta Class
        """

        model = UserSerializer.Meta.model

        fields = tuple(
            set(copy.deepcopy(UserSerializer.Meta.fields))
            - set(
                [
                    "id",
                    "email",
                    "username",
                ]
            )
        )


class RegisterUserSerializer(UserSerializer):

    class Meta:
        """
        Meta Class
        """

        model = UserSerializer.Meta.model

        fields = tuple(
            set(copy.deepcopy(UserSerializer.Meta.fields))
            - set(
                [
                    "id",
                    "is_staff",
                ]
            )
        )

    def create(self, validated_data: dict):
        user: User = super().create(validated_data)
        user.is_staff = False
        user.save()
        return user
