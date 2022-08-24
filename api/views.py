# import DRF Components
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

# Import some AUTH Components
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework.authtoken.models import Token
# from .permissions import IsOwner


# Import Django Components
from .pagination import *
from .models import Users
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Users.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    pagination_class = SmallSetPagination
    queryset = Group.objects.all()


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    # permission_classes = [IsOwner]
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    # permission_classes = [IsOwner]
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.apikey = str(token.key)
        user.save()
        return Response({
                        'user_id': user.pk,
                        'token': token.key,
                        'username': user.username,
                        'email': user.email
                        })


class ImageDataViewSet(viewsets.ModelViewSet):
    serializer_class = ImageDataSerializer
    queryset = ImageData.objects.all()


class MappingDataViewSet(viewsets.ModelViewSet):
    serializer_class = MappingDataSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = MappingData.objects.all()


class ResultDataViewSet(viewsets.ModelViewSet):
    serializer_class = ResultDataSerializer
    pagination_class = StandardSetPagination
    parser_classes = (MultiPartParser, FormParser)
    queryset = ResultData.objects.all()


class TaskHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskHistorySerializer
    pagination_class = StandardSetPagination
    queryset = TaskHistory.objects.all()
