"""Модели для приложения posts."""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

MAX_GROUP_TITLE_LENGTH = 200


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(max_length=MAX_GROUP_TITLE_LENGTH)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Название группы."""
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    """Модель поста."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )  # поле для картинки
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        """Текст поста."""
        return self.text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        """Текст комментария."""
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)
