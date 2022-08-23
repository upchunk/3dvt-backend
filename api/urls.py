from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()

router.register(r'users', UserViewSet, basename='Users')
router.register(r'group', GroupViewSet, basename='Groups')
router.register(r'imagedata', ImageDataViewSet, basename='Image Data')
router.register(r'mappingdata', MappingDataViewSet, basename='Mapping Data')
router.register(r'resultdata', ResultDataViewSet, basename='Result')
router.register(r'taskhistory', TaskHistoryViewSet, basename='Task History')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apikey/', CustomAuthToken.as_view(), name='custom_auth_token'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),
         name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout/all/', LogoutAllView.as_view(), name='auth_logout_all'),
]
urlpatterns += router.urls
