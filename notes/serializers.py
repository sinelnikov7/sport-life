from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """Сериализатор Создания и Обновления заметок"""
    id = serializers.IntegerField(read_only=True)
    time_create = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'text', 'time_create']



# class NoteGetSerializer(serializers.ModelSerializer):
#     """Сериализатор Получение заметок"""
#     class Meta:
#         model = Note
#         fields = '__all__'