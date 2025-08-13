"""ViewSets для API приложения Yatube."""

from typing import Any
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import BaseSerializer

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class AuthorPermissionMixin:
    """Проверка прав автора."""

    def check_author_permission(self, instance: Any) -> None:
        """Валидация прав."""
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')

    def perform_update(self, serializer: BaseSerializer) -> None:
        """Проверка при обновлении."""
        self.check_author_permission(serializer.instance)
        super().perform_update(serializer)

    def perform_destroy(self, instance: Any) -> None:
        """Проверка при удалении."""
        self.check_author_permission(instance)
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """CRUD постов."""

    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Установка автора."""
        serializer.save(author=self.request.user)


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """CRUD комментариев."""

    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet[Comment]:
        """Фильтрация по посту."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id).select_related(
            'author', 'post'
        )

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Установка поста."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post, author=self.request.user)
