from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import UserRegister, UserApprove, UserApiView, UserUpdateView, update, main, UserDelleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from notes.views import NoteCreateUpdateGetDestroyViewSet


router = DefaultRouter()
# router.register("register/", UserRegister, basename='register')
router.register('note', NoteCreateUpdateGetDestroyViewSet, basename='note')


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', UserRegister.as_view()),
    path('auth/approve/', UserApprove.as_view()),
    path('profile/', UserApiView.as_view()),
    path('profile/update/', UserUpdateView.as_view()),
    path('dellete/<int:pk>', UserDelleteView.as_view()),
    # path('git_update', update),
    path('main', main),
    path('', include(router.urls)),
]