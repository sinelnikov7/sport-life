import random

import jwt
from django.db import transaction
from rest_framework import serializers

from sport_life.settings import SECRET_KEY
from .tasks import send_confirm_email
from .models import User, ConfirmCode

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
            user = User(email=validated_data['email'], username=validated_data['username'])
            user.set_password(validated_data['password'])
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

    def approve(self, request):
        """Активация пользователя по коду из письма"""
        token = request.headers.get('Authorization').split(' ')[1]
        user_id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])['user_id']
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
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    is_coach = serializers.BooleanField(default=False)
    date_of_birth = serializers.DateField(required=True)
    height = serializers.DecimalField(max_digits=3, decimal_places=1)
    weight = serializers.DecimalField(max_digits=3, decimal_places=1)
    avatar = serializers.ImageField(required=False)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_coach',
                  'date_of_birth', 'height', 'weight', 'avatar', 'age')

    def update(self, instance, validated_data, request):
        """Обновление пользователя"""
        user_id = instance.id
        token = request.headers.get('Authorization').split(' ')[1]
        user_id_from_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])['user_id']
        if user_id == user_id_from_token:
            super().update(instance, validated_data)
            age = instance.get_age
            setattr(instance, 'age', age)
            return {"success": True, "user": instance}
        else:
            return {"success": False}



