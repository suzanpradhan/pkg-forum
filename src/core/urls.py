from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.core import apis

router = SimpleRouter()
router.register("groups", apis.GroupViewSet)
router.register("permissions", apis.PermissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("content-types", apis.ContentTypeListApi.as_view(), name="list-content-type"),
    path("assign-roles/", apis.AssignRolesToUserApi.as_view(), name="assign-roles"),
    path(
        "user-permissions/<str:username>/",
        apis.AssignPermissionsToUserAPi.as_view(),
        name="user-assign-permissions",
    ),
    path(
        "user-permissions",
        apis.UserPermissionApi.as_view(),
        name="user-permissions",
    ),
]
