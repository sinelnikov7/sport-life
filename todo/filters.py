import django_filters

from todo.models import Task


class TaskFilter(django_filters.FilterSet):
    '''Фильтр заметок'''
    title = django_filters.CharFilter(lookup_expr='icontains', label='Фильтр по полю "Описание задачи"')

    class Meta:
        model = Task
        fields = ['title']