from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from main.models import User

class Friend(models.Model):
    sended_invites = models.ManyToManyField(User, related_name='send_invite', verbose_name="Список отправленных приглашений",  blank=True)
    got_invites = models.ManyToManyField(User, related_name='get_invite', verbose_name="Список полученных приглашений",  blank=True)
    friend_list = models.ManyToManyField(User, related_name='friend_list', verbose_name="Список друзей",  blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, verbose_name="Пользователь",  null=True, blank=True)

    def __str__(self):
        user = User.objects.get(friend__id=self.id)
        return f"{user.first_name} {user.last_name} id={self.id}"

@receiver(post_save, sender=User)
def create_setting(sender, instance, **kwargs):
    """Создание объекта списка друзей для пользователя"""
    try:
        instance.friend
    except ObjectDoesNotExist:
        Friend.objects.create(user_id=instance.id)
# Create your models here.
