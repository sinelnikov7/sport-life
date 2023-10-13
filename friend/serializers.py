from rest_framework import serializers

from .models import Friend
from main.serializers import UserRetrieveSerializer


class GetFriendSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка друзей"""
    sended_invites = UserRetrieveSerializer(many=True)
    got_invites = UserRetrieveSerializer(many=True)
    friend_list = UserRetrieveSerializer(many=True)

    class Meta:
        model = Friend
        exclude = ('id', 'user')