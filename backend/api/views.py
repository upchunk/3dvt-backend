# import DRF Components
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

# Import some AUTH Components
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework.authtoken.models import Token

from drf_spectacular.utils import extend_schema
from .scripts.AIO_Segmentasi import segmentation

# Import Django Components

from api.pagination import SmallSetPagination, StandardSetPagination
from api.serializers import (
    ChangePasswordSerializer,
    GroupSerializer,
    ImageDataSerializer,
    LandingPageSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ResearcherSerializer,
    TaskHistorySerializer,
    UpdateUserSerializer,
    UsersSerializer,
)
from api.models import ImageData, LandingPage, Researcher, TaskHistory, Users
from django.contrib.auth.models import Group

inDevelopment = True


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ("groups",)
    queryset = Users.objects.all()
    if inDevelopment:
        permission_classes = [AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    pagination_class = SmallSetPagination
    queryset = Group.objects.all()
    if inDevelopment:
        permission_classes = [AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    # permission_classes = [IsOwner]
    serializer_class = ChangePasswordSerializer
    if inDevelopment:
        permission_classes = [AllowAny]


class UpdateProfileView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    # permission_classes = [IsOwner]
    serializer_class = UpdateUserSerializer
    if inDevelopment:
        permission_classes = [AllowAny]


class LogoutView(APIView):
    if inDevelopment:
        permission_classes = [AllowAny]

    @extend_schema(exclude=True)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    if inDevelopment:
        permission_classes = [AllowAny]

    @extend_schema(exclude=True)
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

    @extend_schema(
        # extra parameters added to the schema
        description="Get your API Key to Authenticate and access all of the feature",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user.apikey = str(token.key)
        user.save()
        return Response(
            {
                "user_id": user.pk,
                "token": token.key,
                "username": user.username,
                "email": user.email,
            }
        )


class ImageDataViewSet(viewsets.ModelViewSet):
    serializer_class = ImageDataSerializer
    pagination_class = StandardSetPagination
    queryset = ImageData.objects.all()
    filterset_fields = ("user", "groupname")
    if inDevelopment:
        permission_classes = [AllowAny]


class SegmentationTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskHistorySerializer
    pagination_class = StandardSetPagination
    parser_classes = [MultiPartParser, FormParser]
    queryset = TaskHistory.objects.all()
    filterset_fields = ("user", "groupname", "status")
    if inDevelopment:
        permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        userid = request.user.id
        user = Users.objects.get(pk=userid)
        group = Group.objects.get(user=user)
        task = TaskHistory.objects.create(
            user=user, status="RECIEVED", type="segmentation"
        )
        images = request.FILES.getlist("images")
        print(images)
        source_list = []
        result_list = []
        try:
            for img in images:
                result = segmentation(user, img, task)
                if result:
                    status = "SUCCESS"
                    source_list.append(
                        {
                            "name": str(img),
                            "original": result.images.url,
                            "originalHeight": 448,
                            "originalWidth": 448,
                        }
                    )
                    result_list.append(
                        {
                            "name": str(img),
                            "original": result.result.url,
                            "originalHeight": 448,
                            "originalWidth": 448,
                        }
                    )
                else:
                    status = "FAILED"

            if status == "SUCCESS":
                task.sources = source_list
                task.results = result_list
                task.status = status
                task.groupname = group.name
                task.save()
                serializer = self.get_serializer(instance=task)
                return Response(
                    {
                        "status": "SUCCESS",
                        "message": "Image(s) segmentation completed successfully",
                        "task_data": serializer.data,
                    }
                )
            else:
                return Response(
                    {"status": "FAILED", "message": "Internal Server Error"}
                )
        except:
            raise Exception("An error occurred")


class ReconstructionTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskHistorySerializer
    pagination_class = StandardSetPagination
    queryset = TaskHistory.objects.all()
    filterset_fields = ("groupname", "status")
    if inDevelopment:
        permission_classes = [AllowAny]


class ResearcherViewSet(viewsets.ModelViewSet):
    serializer_class = ResearcherSerializer
    pagination_class = StandardSetPagination
    queryset = Researcher.objects.all()
    if inDevelopment:
        permission_classes = [AllowAny]


class LandingPageViewSet(viewsets.ModelViewSet):
    serializer_class = LandingPageSerializer
    pagination_class = StandardSetPagination
    queryset = LandingPage.objects.all()
    if inDevelopment:
        permission_classes = [AllowAny]
