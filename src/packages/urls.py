from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .apis import PackageAPISet

router = SimpleRouter()
router.register("packages", PackageAPISet)

urlpatterns = [
    path("", include(router.urls)),
]
