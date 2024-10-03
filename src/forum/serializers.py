from rest_framework import serializers

from src.forum.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """ "
    Serializer for Post
    """

    class Meta:
        """
        Meta Class
        """

        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """ "
    Serializer for Comment
    """

    class Meta:
        """
        Meta Class
        """

        model = Comment
        fields = "__all__"
