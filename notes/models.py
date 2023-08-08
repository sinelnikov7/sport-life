from django.db import models

from main.models import User


class Note(models.Model):
    """Заметки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    text = models.TextField(verbose_name='Текст заметки')
    time_create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True) #'2023-07-31 12:34:56'

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ['id']

    def __str__(self):
        preview = self.text
        if len(preview) > 20:
            preview = preview[0:20:1]
        return f"{preview}"
# Create your models here.
