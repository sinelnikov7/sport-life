from django.db import models

class ImageExercise(models.Model):
    """Озображения упражнений"""
    image = models.ImageField(upload_to='exercise')


class ComentExercise(models.Model):
    """Комментарий к упражнению"""
    coment = models.TextField(verbose_name='Коментраий')
    exercise = models.ForeignKey('Exercise', verbose_name='Упражнение', on_delete=models.CASCADE)


class Exercise(models.Model):
    """Модель упрожнений"""
    name = models.CharField(max_length=100, verbose_name='Название упражнения')
    description = models.TextField(verbose_name='Описание')
    likes = models.IntegerField(default=0, verbose_name='Количество лайков')
    image_exercises = models.ManyToManyField('ImageExercise', verbose_name='Изображения упражнений')
    add_to_favorites = models.ManyToManyField('User', verbose_name='Добавлены в избранное у пользователей')

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self):
        return f"{self.name}"
# Create your models here.
