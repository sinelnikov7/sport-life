from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserRegister, UserApprove, UserApiView, UserUpdateView, update, main

router = DefaultRouter()


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('approve/', UserApprove.as_view()),
    path('user_detail/<int:pk>', UserApiView.as_view()),
    path('user_update/<int:pk>', UserUpdateView.as_view()),
    path('git_update', update),
    path('main', main),
]