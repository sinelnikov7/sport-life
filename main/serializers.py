import random

import jwt
from django.db import transaction
from rest_framework import serializers


from sport_life.settings import SECRET_KEY
from .tasks import send_confirm_email
from .models import User, ConfirmCode

from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.settings import api_settings

def email_unique_validitor(data: str):
    """Валидация email на уникальность при регистрации"""
    if User.objects.filter(email=data.lower()).exists():
        raise serializers.ValidationError("Пользователь с таким email уже зарегестрирован")
    else:
        return data.lower()

def username_unique_validitor(data: str):
    """Валидация username на уникальность при регистрации"""
    if User.objects.filter(username=data.lower()).exists():
        raise serializers.ValidationError("Пользователь с таким username уже зарегестрирован")
    else:
        return data.lower()

class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя"""
    email = serializers.EmailField(validators=[email_unique_validitor])
    # email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=150, validators=[username_unique_validitor])
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        """Регистрация нового пользователя, создание проверочного кода
            и отправка кода на почту новому пользователю"""
        with transaction.atomic():
            user = User(email=validated_data['email'].lower(), username=validated_data['username'].lower())
            user.set_password(validated_data['password'].lower())
            user.save()
            user_id = user.id
            number = random.randint(1000, 9999)
            code = ConfirmCode(user_id=user_id, key=number)
            code.save()
            # send_confirm_email.delay(to_email=validated_data['email'], send_code=number, password=validated_data['password'])
            send_confirm_email(to_email=validated_data['email'], send_code=number, password=validated_data['password'])
        return user

class ApproveSerializer(serializers.ModelSerializer):
    """Сериализатор кода активации пользователя"""

    class Meta:
        model = ConfirmCode
        fields = ('key', )

    def approve(self, request, user_id):
        """Активация пользователя по коду из письма"""
        key = int(request.data['key'])
        code = ConfirmCode.objects.get(user_id=user_id).key
        if code == key:
        # if key == 1234:
            user = User.objects.get(id=user_id)
            user.is_approve = True
            user.save()
            return {"success": True}
        else:
            return {"success": False, "message": "Неверный пароль"}



class UserRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор обновления пользователя"""
    email = serializers.EmailField(read_only=True)
    is_approve = serializers.BooleanField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    is_coach = serializers.BooleanField(default=False)
    date_of_birth = serializers.DateField(required=True)
    height = serializers.DecimalField(max_digits=4, decimal_places=1)
    weight = serializers.DecimalField(max_digits=4, decimal_places=1)
    avatar = serializers.ImageField(required=False)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'is_approve', 'username', 'email', 'first_name', 'last_name', 'is_coach',
                  'date_of_birth', 'height', 'weight', 'avatar', 'age')

    def update(self, instance, validated_data, user_id):
        """Обновление пользователя"""
        if user_id == instance.id:
            super().update(instance, validated_data)
            age = instance.get_age
            setattr(instance, 'age', age)
            return {"success": True, "user": instance}
        else:
            return {"success": False}


# class TokenSerializer(serializers.Serializer):
#     """Сириализатор для получения токена"""
#     username_field = get_user_model().USERNAME_FIELD
#     token_class = None
#
#     default_error_messages = {
#         "no_active_account": ("No active account found with the given credentials")
#     }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields[self.username_field] = serializers.CharField()
#         self.fields["password"] = PasswordField()
#     def validate(self, attrs):
#         authenticate_kwargs = {
#             self.username_field: attrs[self.username_field].lower(),
#             "password": attrs["password"],
#         }
#         try:
#             authenticate_kwargs["request"] = self.context["request"]
#         except KeyError:
#             pass
#
#         self.user = authenticate(**authenticate_kwargs)
#
#         if not api_settings.USER_AUTHENTICATION_RULE(self.user):
#             raise exceptions.AuthenticationFailed(
#                 self.error_messages["no_active_account"],
#                 "no_active_account",
#             )
#         return {}
#
#     @classmethod
#     def get_token(cls, user):
#         return cls.token_class.for_user(user)



