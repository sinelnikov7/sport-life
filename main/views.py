import jwt
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from sport_life.settings import SECRET_KEY
from .models import ConfirmCode, User, Setting
from .serializers import UserRegistrationSerializer, ApproveSerializer, UserRetrieveSerializer, SettingGetSerializer

import git
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import dotenv
import os

from .services import get_user_id

dotenv.load_dotenv()
REPO = os.environ.get('REPO')

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
        repo = git.Repo(REPO)
        # repo = git.Repo("./sport-life")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


class UserRegister(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

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
        user_id = get_user_id(request)
        if serializer.is_valid():
            response = serializer.approve(request, user_id)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=status.HTTP_200_OK)



class UserApiView(generics.RetrieveAPIView):
    """Получение данных пользователя пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user_id = get_user_id(request)
        try:
            queryset = User.objects.get(id=user_id)
            if queryset.date_of_birth != None:
                age = queryset.get_age
                setattr(queryset, 'age', age)
            serializer = self.serializer_class(queryset)
            print(queryset.setting.city, queryset.setting.country, queryset.setting.who_can_watch)
            return Response({"status": 200, "user": serializer.data})
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class UserUpdateView(generics.UpdateAPIView):
    """Обновление пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user_id = get_user_id(request)
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            response = serializer.update(User.objects.get(id=user_id), serializer.validated_data, user_id)
        else:
            return Response({"errors": serializer.errors})
        if response["success"]:
            user = response["user"]
            return Response(UserRetrieveSerializer(user).data)
        else:
            return Response({"success": False, "message": "Неверный token пользователя"})


class UserDelleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    # permission_classes = (IsAuthenticated,)
    def destroy(self, request, *args, **kwargs):

        user_id = kwargs['pk']
        try:
            User.objects.get(id=user_id).delete()
            return Response({"status": 200, "user": "Удален"})
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def user_setting_update(request):
    """Обновление пользовательских настроек"""
    user_id = get_user_id(request)
    serializer = SettingGetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.update(Setting.objects.get(user_id=user_id), serializer.validated_data)
        q = Setting.objects.get(user_id=user_id)
        print(q.user.email)
        return Response({"settings": serializer.data})
    else:
        response = serializer.errors
        return Response(response)