from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from api.views import (
    ChangePasswordView,
    CustomAuthToken,
    GroupViewSet,
    ImageDataViewSet,
    LandingPageViewSet,
    LogoutAllView,
    LogoutView,
    MyTokenObtainPairView,
    ReconstructionTaskViewSet,
    RegisterView,
    ResearcherViewSet,
    SegmentationTaskViewSet,
    UpdateProfileView,
    UserViewSet,
)


router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"group", GroupViewSet, basename="groups")
router.register(r"images", ImageDataViewSet, basename="image_data")
router.register(r"segmentation", SegmentationTaskViewSet, basename="segmentation_tasks")
router.register(
    r"reconstruction", ReconstructionTaskViewSet, basename="reconstruction_tasks"
)
router.register(r"researcher", ResearcherViewSet, basename="researcher")
router.register(r"landingPage", LandingPageViewSet, basename="landing_pages")

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("apikey/", CustomAuthToken.as_view(), name="custom_auth_token"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    path(
        "update_profile/<int:pk>/",
        UpdateProfileView.as_view(),
        name="auth_update_profile",
    ),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("logout/all/", LogoutAllView.as_view(), name="auth_logout_all"),
]
urlpatterns += router.urls
