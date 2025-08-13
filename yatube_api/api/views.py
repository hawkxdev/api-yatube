"""ViewSets для API приложения Yatube."""

from typing import Any
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import BaseSerializer

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """CRUD постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Установка автора."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer: BaseSerializer) -> None:
        """Проверка прав."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, instance: Any) -> None:
        """Проверка прав."""
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD комментариев."""

    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet[Comment]:
        """Фильтрация по посту."""
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Установка поста."""
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, author=self.request.user)

    def perform_update(self, serializer: BaseSerializer) -> None:
        """Проверка прав."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, instance: Any) -> None:
        """Проверка прав."""
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        super().perform_destroy(instance)
