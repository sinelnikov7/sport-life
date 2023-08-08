import django_filters

from notes.models import Note


class NoteFilter(django_filters.FilterSet):

    text = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Note
        fields = ['text']