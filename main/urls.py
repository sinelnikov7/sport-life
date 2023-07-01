from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegister, UserApprove, UserApiView, UserUpdateView, update, main, UserDelleteView

router = DefaultRouter()
# router.register("register/", UserRegister, basename='register')


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('approve/', UserApprove.as_view()),
    path('profile/', UserApiView.as_view()),
    path('profile/update/', UserUpdateView.as_view()),
    path('dellete/<int:pk>', UserDelleteView.as_view()),
    path('git_update', update),
    path('main', main),
    path('api/', include(router.urls)),
]