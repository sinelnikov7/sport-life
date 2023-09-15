from django.urls import path, include
from rest_framework.routers import DefaultRouter

from router.router import router
from .views import UserRegister, UserApprove, UserApiView, UserUpdateView, update, main, UserDelleteView
#
# router = DefaultRouter()
# # router.register("register/", UserRegister, basename='register')
#
#
urlpatterns = [
    path('git_update', update),
]