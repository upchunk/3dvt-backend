from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')
router.register(r'dataset', views.DataViewSet, basename='dataset')
router.register(r'result', views.ResultViewSet, basename='result')

urlpatterns = []
urlpatterns += router.urls
