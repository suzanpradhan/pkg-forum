from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostAPISet(viewsets.ModelViewSet):
    """
    Model View Set for Post
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = []
    lookup_field = "pk"
    http_method_names = ("get", "post", "patch", "delete")
    filter_backends = (SearchFilter,)
    search_fields = ("title",)


class CommentAPISet(viewsets.ModelViewSet):
    """
    Model View Set for Comment
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = []
    lookup_field = "pk"
    http_method_names = ("get", "post", "patch", "delete")
    filter_backends = (SearchFilter,)
    search_fields = ("content",)
