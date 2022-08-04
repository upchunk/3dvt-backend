from .pagination import *
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Users.objects.all()


class DataViewSet(viewsets.ModelViewSet):
    serializer_class = DataSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = ImageData.objects.all()
