from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from main.views import UserRegister, UserApprove, UserApiView, UserUpdateView, update, main, UserDelleteView, user_setting_update
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from notes.views import NoteCreateUpdateGetDestroyViewSet
from todo.views import TaskCreateUpdateGetDestroyViewSet

from friend.views import get_friends, add_to_friendlist, confirm_to_friendlist


router = DefaultRouter()
# router = SimpleRouter()
# router.register("register/", UserRegister, basename='register')
router.register('note', NoteCreateUpdateGetDestroyViewSet, basename='note')
router.register('task', TaskCreateUpdateGetDestroyViewSet, basename='task')


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', UserRegister.as_view()),
    path('auth/approve/', UserApprove.as_view()),
    path('profile/', UserApiView.as_view()),
    path('profile/update/', UserUpdateView.as_view()),
    path('profile/setting-update/', user_setting_update),
    path('dellete/<int:pk>', UserDelleteView.as_view()),
    # path('git_update', update),
    path('main', main),
    path('', include(router.urls)),

    path('get-friends/', get_friends),
    path('add-to-friendlist/<int:pk>', add_to_friendlist),
    path('confirm-to-friendlist/<int:pk>', confirm_to_friendlist)
]