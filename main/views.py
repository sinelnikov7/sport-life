from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from .models import ConfirmCode, User
from .serializers import UserRegistrationSerializer, ApproveSerializer, UserRetrieveSerializer

import git
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def main(request):
    return render(request, 'main.html')
@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("test.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")




class UserRegister(APIView):

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        """Регистрация нового пользователя"""
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            response = serializer.create(validated_data=serializer.validated_data)
            return Response({"User": UserRegistrationSerializer(response).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors})


class UserApprove(APIView):
    """Подтверждение регистрации, проверка соответствия кода из письма у пользователя"""
    queryset = ConfirmCode.objects.all()
    serializer_class = ApproveSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=ApproveSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = serializer.approve(request)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=status.HTTP_200_OK)


class UserApiView(generics.RetrieveAPIView):
    """Получение данных пользователя пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):

        user_id = kwargs['pk']
        try:
            queryset = User.objects.get(id=user_id)
            if queryset.date_of_birth != None:
                age = queryset.get_age
                setattr(queryset, 'age', age)
            serializer = self.serializer_class(queryset)
            return Response({"status": 200, "user": serializer.data})
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)



class UserUpdateView(generics.UpdateAPIView):
    """Обновление пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = serializer.update(User.objects.get(id=kwargs["pk"]), serializer.validated_data, request)
        else:
            return Response({"errors": serializer.errors})
        if response["success"]:
            user = response["user"]
            return Response(UserRetrieveSerializer(user).data)
        else:
            return Response({"success": False, "message": "Неверный token пользователя"})
