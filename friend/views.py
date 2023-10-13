from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from .serializers import GetFriendSerializer
from main.services import get_user_id
from .models import Friend
from main.models import User

@api_view(['get'])
def get_friends(request):
    """Получить список друзей"""
    user_id = get_user_id(request)
    queryset = Friend.objects.get(user_id=user_id)
    response = GetFriendSerializer(queryset).data
    return Response({'data': response})


@api_view(['get'])
def add_to_friendlist(request, pk):
    """Отправить запрос на добавление в список друзей"""
    user_id = get_user_id(request)
    queryset = Friend.objects.get(user_id=user_id)
    try:
        if pk in queryset.sended_invites.values_list('id', flat=True):
            return Response({"error": {'message': f"Вы уже отправили приглашение пользователю с id={pk}"}})
        elif pk in queryset.got_invites.values_list('id', flat=True):
            return Response({"error": {'message': f"Пользователь с id={pk} уже отправил вам приглашение"}})
        elif pk in queryset.friends.values_list('id', flat=True):
            return Response({"error": {'message': f"Пользователь с id={pk} уже в списке ваших друзей"}})
        elif pk == user_id:
            return Response({"error": {'message': f"Нельзя добавить в список друзей самого себя"}})
        else:
            with transaction.atomic():
                queryset.sended_invites.add(User.objects.get(id=pk))
                Friend.objects.get(user_id=pk).got_invites.add(User.objects.get(id=user_id))
            response = GetFriendSerializer(queryset).data
            return Response({'data': response})
    except ObjectDoesNotExist:
        return Response({"error": {"message": f"Пользователя с id={pk} не существует"}})


@api_view(['get'])
def confirm_to_friendlist(request, pk):
    """Подтвердить запрос на добавление в список друзей"""
    user_id = get_user_id(request)
    queryset_recepient = Friend.objects.get(user_id=user_id)
    queryset_sender = Friend.objects.get(user_id=pk)
    sender = User.objects.get(id=pk)
    recipient = User.objects.get(id=user_id)
    if pk not in queryset_recepient.got_invites.values_list('id', flat=True):
        return Response({"error": {'message': f"Пользователя с id={pk} нету в списке полученных приглашений"}})
    else:
        with transaction.atomic():
            queryset_recepient.got_invites.remove(sender)
            queryset_sender.sended_invites.remove(recipient)
            queryset_recepient.friends.add(sender)
            queryset_sender.friends.add(recipient)
        response = GetFriendSerializer(queryset_recepient).data
        return Response({'data': response})
