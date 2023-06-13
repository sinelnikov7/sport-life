from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import register, UserApprove, UserApiView, UserUpdateView

router = DefaultRouter()


urlpatterns = [
    path('register/', register),
    path('approve/', UserApprove.as_view()),
    path('user_detail/<int:pk>', UserApiView.as_view()),
    path('user_update/<int:pk>', UserUpdateView.as_view()),
]