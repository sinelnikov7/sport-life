import django_filters

from todo.models import Task


class TaskFilter(django_filters.FilterSet):
    '''Фильтр задач'''
    date = django_filters.DateFilter(label='Фильтр по дате исполнения задачи')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Фильтр по полю "Описание задачи"')


    class Meta:
        model = Task
        fields = ['title', 'status_id', 'priority_id']