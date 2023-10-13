import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser
from django.db import models

# from friend.models import Friend



class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(verbose_name="email address", unique=True)
    is_approve = models.BooleanField(default=False, verbose_name='Пользователь подтвердил код из письма')
    is_coach = models.BooleanField(verbose_name="Являеться ли пользователь тренером",default=False)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Рост в см', null=True, blank=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Вес в кг', null=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatar', verbose_name='Аватар пользователя', null=True, blank=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.id}"




    @property
    def get_age(self):
        """Узнать текущий возраст"""
        age = datetime.date.today() - self.date_of_birth
        return age.days // 365


class ConfirmCode(models.Model):
    """Код активации пользователя после регистрации, приходит на почту"""
    key = models.IntegerField(verbose_name='Проверочный код')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = "Код активации пользователя"
        verbose_name_plural = "Коды активации пользователей"

    def __str__(self):
        return f'Пароль для активации пользователя id = {self.user_id}'


class Setting(models.Model):
    """Модель настроек пользователя"""
    choice_watch = (
        (0, "Могут видеть все"),
        (1, "Могут видеть только друзья"),
        (2, "Никто не может видеть"),
    )
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город")
    who_can_watch = models.IntegerField(null=True, blank=True, choices=choice_watch,
                                     verbose_name="Кто может смотреть страницу")
    user = models.OneToOneField('User', on_delete=models.SET_NULL, verbose_name="Пользователь", null=True, blank=True)

    def __str__(self):
        user = User.objects.get(setting__id=self.id)
        return f"{user.first_name} {user.last_name} id={self.id}"

@receiver(post_save, sender=User)
def create_setting(sender, instance, **kwargs):
    """Создание объекта настроек для пользователя"""
    try:
        instance.setting
    except ObjectDoesNotExist:
        Setting.objects.create(who_can_watch=0, user_id=instance.id)







# Create your models here.

