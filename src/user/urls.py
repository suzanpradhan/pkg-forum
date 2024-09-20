from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView

from src.user import apis

router = SimpleRouter()
router.register("accounts", apis.UserViewSet)
router.register("profiles", apis.ProfileViewSet)

auth_urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", apis.RegisterUser.as_view(), name="register_user"),
]

urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    path(
        "password_reset", apis.PasswordResetRequestView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        apis.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", include(router.urls)),
    path("accounts/all", apis.GetAllUser.as_view(), name="get_all_users"),
]
