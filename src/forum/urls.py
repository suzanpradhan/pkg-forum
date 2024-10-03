from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .apis import PostAPISet, CommentAPISet

router = SimpleRouter()
router.register("posts", PostAPISet)
router.register("comments", CommentAPISet)

urlpatterns = [
    path("", include(router.urls)),
]
