from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from src.core.serializers import (
    ContentTypeSerializer,
    GroupSerializer,
    PermissionSerializer,
)
from src.core.viewsets import ZenModelViewSet
from src.user.models import User
from src.user.serializers import PermissionListSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    Model View Set for Permissions
    """

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "codename"
    http_method_names = ("get", "post")


class GroupViewSet(ZenModelViewSet):
    """
    Model View Set for Group
    """

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "pk"
    http_method_names = ("get", "post", "patch", "delete")

    def list(self, request, *args, **kwargs):
        return super().list(request, fields=("id", "name"), *args, **kwargs)


class ContentTypeListApi(generics.ListAPIView):
    """
    List API for Content Types
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()
    pagination_class = None


class AssignRolesToUserApi(generics.GenericAPIView):
    """
    Assign Roles to User API
    """

    serializer_class = PermissionListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """
        Post Method
        """
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data: dict = serializer.data
            user = validated_data["user"]
            group = validated_data["group"]
            user.groups.add(group)

            return Response(
                {"message": f"{group.name} role has been assigned to {user.username}."},
                status=status.HTTP_200_OK,
            )


class UserPermissionApi(generics.GenericAPIView):
    """
    Get List of Permissions
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get Permissions Names
        """
        if request.user.groups.exists():
            serializer = PermissionSerializer(
                request.user.groups.first().permissions,
                fields=("id", "codename"),
                many=True,
            )
        else:
            group = Group.objects.create(name=request.user)
            request.user.groups.add(group)
            serializer = PermissionSerializer(
                group.permissions, fields=("id", "codename"), many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignPermissionsToUserAPi(generics.GenericAPIView):
    """
    Directly Assign Permissions to User API
    """

    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, username):
        """
        Post Method
        """
        with transaction.atomic():
            user = User.objects.filter(username=username).first()
            if user.groups.exists():
                group = user.groups.first()
                serializer = self.get_serializer(group, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                request.data["name"] = user.username
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                group = serializer.save()
                user.groups.add(group)
            return Response(
                {"message": f"Permissions has been assigned to {user.username}."},
                status=status.HTTP_200_OK,
            )

    def get(self, request, username):
        """
        Get Method
        """
        user = User.objects.filter(username=username).first()
        if user.groups.exists():
            serializer = self.get_serializer(user.groups.first())
        else:
            group = Group.objects.create(name=username)
            user.groups.add(group)
            serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
