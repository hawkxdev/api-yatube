"""Сериализаторы для API приложения Yatube."""

from rest_framework import serializers

from posts.models import Comment, Group, Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор групп."""

    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "text", "pub_date", "author", "image", "group")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "text", "created")
        read_only_fields = ("post",)
