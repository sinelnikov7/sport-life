import django_filters

from notes.models import Note


class NoteFilter(django_filters.FilterSet):
    '''Фильтр заметок'''
    text = django_filters.CharFilter(lookup_expr='icontains', label='Фильтр по полю "Текст"')

    class Meta:
        model = Note
        fields = ['text']