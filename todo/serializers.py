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


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания, обновления задач"""
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    priority_id = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    time = serializers.TimeField()
    class Meta:
        model = Task
        fields = ['id', 'user_id', 'date', 'time', 'title', 'status_id', 'priority_id']

    def create(self, validated_data, user_id):
        task = Task(user_id=user_id, date=validated_data['date'], time=validated_data['time'],
                    title=validated_data['title'], status=validated_data['status_id'],
                    priority=validated_data['priority_id'])
        task.save()
        return task

class TaskGetSerializer(serializers.ModelSerializer):
    """Сериализатор  получения задач"""
    status = StatusSerializer()
    priority = PrioritySerializer()
    class Meta:
        model = Task
        # fields = '__all__'
        exclude = ('user', )
        # depth = 2


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор  обновления задач"""
    time = serializers.TimeField(required=False)
    date = serializers.DateField(required=False)
    title = serializers.CharField(required=False)
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), required=False)
    priority_id = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all(), required=False)

    class Meta:
        model = Task
        exclude = ('user', 'status', 'priority')
        # depth = 2

