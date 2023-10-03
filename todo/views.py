from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from main.services import get_user_id
from .paginators import TaskPagination
from .serializers import TaskCreateSerializer, TaskGetSerializer, TaskUpdateSerializer
from .models import Task
from .filters import TaskFilter

class TaskCreateUpdateGetDestroyViewSet(mixins.CreateModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    serializer_class = TaskCreateSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # IsOwnerFilterBackend ]
    # filterset_fields = ['text']
    ordering_fields = ['date', 'time']
    filterset_class = TaskFilter

    def create(self, request, *args, **kwargs):
        """Создание задачи"""
        serializer = TaskCreateSerializer(data=request.data)
        user_id = get_user_id(request)
        if serializer.is_valid():
            task = serializer.create(serializer.validated_data, user_id)
            return Response(TaskGetSerializer(task).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors})

    def list(self, request, *args, **kwargs):
        """Получение списка задач"""
        # user_id = 3
        user_id = get_user_id(request)
        tasks = self.filter_queryset(Task.objects.filter(user_id=user_id))
        page = self.paginate_queryset(tasks)
        response = TaskGetSerializer(page, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return self.get_paginated_response(response.data)

    def partial_update(self, request, *args, **kwargs):
        """Обновление задачи"""
        user_id = get_user_id(request)
        task_id = kwargs.get('pk')
        serializer = TaskUpdateSerializer(data=request.data)
        try:
            instanse = Task.objects.get(id=task_id)
            if instanse.user_id == user_id:
                if serializer.is_valid():
                    serializer.update(instanse, serializer.validated_data)
                    task = Task.objects.get(id=task_id)
                    return Response(TaskGetSerializer(task).data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"errors": serializer.errors})
            else:
                return Response({'error': f'Вы не имеете доступа к записи с id = {task_id}'})
        except ObjectDoesNotExist:
            return Response({'error': f'Записи с id = {task_id} не найдено'})

    def destroy(self, request, *args, **kwargs):
        """Удаление задачи"""
        note_id = kwargs.get('pk')
        user_id = get_user_id(request)
        try:
            instanse = Task.objects.get(id=note_id)
            if instanse.user_id == user_id:
                instanse.delete()
            else:
                return Response({'error': f'Вы не имеете доступа к записи с id = {note_id}'})
        except ObjectDoesNotExist:
            return Response({'error': f'Записи с id = {note_id} не найдено'})
        return Response({'success': True}, status=status.HTTP_200_OK)
