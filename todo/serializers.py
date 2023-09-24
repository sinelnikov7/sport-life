from rest_framework import serializers
from .models import Status, Priority, Task


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор получения статусов"""

    class Meta:
        model = Status
        fields = ['id', 'title']


class PrioritySerializer(serializers.ModelSerializer):
    """Сериализатор получения приоритетов"""

    class Meta:
        model = Priority
        fields = ['id', 'title']


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор создания, обновления и получения приоритетов"""
    id = serializers.IntegerField(read_only=True)
    status = StatusSerializer(many=False)
    priority = Priority(many=False)

    class Meta:
        model = Task
        fields = '__all__'