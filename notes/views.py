from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import NoteFilter
from .models import Note
from .paginators import NotePagination
from .serializers import NoteSerializer
from main.services import get_user_id


class NoteCreateUpdateGetDestroyViewSet(mixins.CreateModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = NotePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # IsOwnerFilterBackend ]
    filterset_fields = ['text']
    ordering_fields = ['time_create']
    filterset_class = NoteFilter

    def create(self, request, *args, **kwargs):
        serializer = NoteSerializer(data=request.data)
        user_id = get_user_id(request)
        if serializer.is_valid():
            note = Note(user_id=user_id, text=serializer.validated_data['text'])
            note.save()
            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors})

    def get(self, request, *args, **kwargs):
        user_id = get_user_id(request)
        notes = Note.objects.filter(user_id=user_id)
        response = NoteSerializer(notes, many=True)
        return Response(response.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        note_id = kwargs.get('pk')
        user_id = get_user_id(request)
        serializer = NoteSerializer(data=request.data)
        try:
            instanse = Note.objects.get(id=note_id)
            if instanse.user_id == user_id:
                if serializer.is_valid():
                    response = serializer.update(instanse, serializer.validated_data)
                    return Response(NoteSerializer(response).data, status=status.HTTP_200_OK)
                else:
                    return Response({"errors": serializer.errors})
            else:
                return Response({'error': f'Вы не имеете доступа к записи с id = {note_id}'})
        except ObjectDoesNotExist:
            return Response({'error': f'Записи с id = {note_id} не найдено'})

    def destroy(self, request, *args, **kwargs):
        note_id = kwargs.get('pk')
        user_id = get_user_id(request)
        try:
            instanse = Note.objects.get(id=note_id)
            if instanse.user_id == user_id:
                instanse.delete()
            else:
                return Response({'error': f'Вы не имеете доступа к записи с id = {note_id}'})
        except ObjectDoesNotExist:
            return Response({'error': f'Записи с id = {note_id} не найдено'})
        return Response({'success': True}, status=status.HTTP_200_OK)
