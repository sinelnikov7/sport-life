from django.db import models

from main.models import User


class Status(models.Model):
    """Статус задачи"""
    title = models.CharField(max_length=20, verbose_name='Название статуса')

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['id']

    def __str__(self):
        return self.title


class Priority(models.Model):
    """Приоритет задачи"""
    title = models.CharField(max_length=20, verbose_name='Название приоритета')

    class Meta:
        verbose_name = "Приоритет"
        verbose_name_plural = "Приоритеты"
        ordering = ['id']

    def __str__(self):
        return self.title


class Task(models.Model):
    """Задачи"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    date = models.DateField(verbose_name='Дата задачи', auto_now_add=False)
    time = models.TimeField(verbose_name='Время задачи', auto_now_add=False)
    title = models.TextField(verbose_name='Описание задачи')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, verbose_name='Приоритет')

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['id']

    def __str__(self):
        preview = self.title
        if len(preview) > 30:
            preview = preview[0:30:1] + '...'
        return f"{preview}"

# Create your models here.
