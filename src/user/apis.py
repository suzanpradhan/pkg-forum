import base64
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.user.models import Profile, User

from .serializers import (PasswordResetRequestSerializer,
                          PasswordResetSerializer, ProfileSerializer,
                          RegisterUserSerializer, UserSerializer)


class PasswordResetRequestView(APIView):
    """
    API view for requesting password reset
    """

    http_method_names = ["post"]
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        """
        Handle Post Request
        """

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_428_PRECONDITION_REQUIRED
            )

        associated_users = get_user_model().objects.filter(
            Q(email=serializer.data["email"])
        )

        if associated_users.exists():
            user = associated_users.first()
            subject = "BuddhaAir HelpDesk - Password Reset Request"
            email_template_name = "password_reset_email.txt"
            context = {
                "email": user.email,
                "domain": get_current_site(request),
                "site_name": "BuddhaAir HelpDesk",
                "uid": base64.urlsafe_b64encode(force_bytes(user.pk)).decode(),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "http",
            }
            email = render_to_string(email_template_name, context)

            try:
                send_mail(
                    subject,
                    email,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return Response(
                    {"message": "Email sent successfully."},
                    status=status.HTTP_200_OK,
                )

            except BadHeaderError:
                print("Invalid header found.")
            except SMTPException:
                return Response(
                    {"message": "Failed to sent email."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception:
                return Response(
                    {"message": "Failed to sent email."},
                    status=status.HTTP_412_PRECONDITION_FAILED,
                )

        else:
            return Response(
                {"message": "User doesn't exist"},
                status=status.HTTP_412_PRECONDITION_FAILED,
            )


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    """
    API View for Reset Password Confirmation and Resetting Password
    """

    if request.method == "GET":
        user = User.objects.filter(
            id=force_str(base64.urlsafe_b64decode(uidb64).decode())
        ).first()

        if not default_token_generator.check_token(user, token):
            return Response(
                {"message": "User don't exist"},
                status=status.HTTP_412_PRECONDITION_FAILED,
            )

        return Response(
            {"message": "Password Reset Request Confirmed"}, status=status.HTTP_200_OK
        )

    if request.method == "POST":
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_428_PRECONDITION_REQUIRED
            )

        user = User.objects.filter(
            id=force_str(base64.urlsafe_b64decode(uidb64).decode())
        ).first()
        if not default_token_generator.check_token(user, token):
            return Response(
                {"message": "User don't exist"},
                status=status.HTTP_412_PRECONDITION_FAILED,
            )

        user.set_password(request.POST.get("new_password1"))
        user.save()

        return Response(
            {"message": "Password Reset Request Confirmed"},
            status=status.HTTP_200_OK,
        )

    return Response({"message": "Token Invalid"}, status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
    """
    Model View Set for User Model
    """

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ("get", "post", "patch", "delete")
    filter_backends = (SearchFilter,)
    search_fields = ("username", "profile__full_name")

    def retrieve(self, request, username, *args, **kwargs):
        if request.user and username == "me":
            instance = request.user
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Model View Set for Profile Model
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    http_method_names = ("get", "post", "patch", "delete")
    filter_backends = (SearchFilter,)
    search_fields = ("full_name", "secondary_email")

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        instance = self.request.user
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        serializer_class=ProfileSerializer,
    )
    def me_update(self, request):
        instance = self.request.user

        if instance.profile:
            serializer = ProfileSerializer(
                instance.profile, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            instance.profile = Profile.objects.create(**request.data)
            serializer = ProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            profile = serializer.save()
            instance.profile = profile
            instance.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class GetAllUser(generics.ListAPIView):
    """
    Get All User
    """

    pagination_class = None
    http_method_names = ("get",)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [IsAuthenticated, IsAdminUser]


class RegisterUser(generics.CreateAPIView):

    serializer_class = RegisterUserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
