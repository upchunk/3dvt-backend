from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group


def uploaded():
    now = arrow.now()
    return now.format('YYYY-MM-DD-HH-mm-ss')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())],
        help_text="Insert your Email Address",
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], help_text="Insert password for this user account")
    password2 = serializers.CharField(
        write_only=True, required=True, help_text="Confirm password for this user account")

    class Meta:
        model = Users
        fields = ('username', 'password', 'password2', 'full_name',
                  'email', "institution")

        extra_kwargs = {
            'username': {"help_text": "Insert username for this account"},
            'full_name': {"help_text": "Insert full name for this account"},
            'institution': {"allow_blank": True, "help_text": 'Insert institution name for this account'},
        }

    def validate(self, attrs: dict):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            institution=validated_data['institution'],
        )

        user.set_password(validated_data['password'])
        user.save()

        group, _ = Group.objects.get_or_create(
            name=validated_data["institution"])
        group.user_set.add(user)
        group.save()

        # Save Auto Generated APIKey to Model
        token, _ = Token.objects.get_or_create(user=user)
        user.apikey = str(token.key)
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], help_text="Insert new password")
    password2 = serializers.CharField(
        write_only=True, required=True, help_text="Confirm new password")
    old_password = serializers.CharField(
        write_only=True, required=True, help_text="Insert old password")

    class Meta:
        model = Users
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        try:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})

            return attrs
        except:
            raise serializers.ValidationError(
                {"This fields may not be blank."})

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, help_text="Email address of the user")

    class Meta:
        model = Users
        fields = ('username', 'full_name', 'email', 'institution')
        extra_kwargs = {
            'username': {"help_text": "Username for this account"},
            'full_name': {"required": True, "help_text": "User's full name"},
            'institution': {"allow_blank": True, "help_text": "User's institution name"}
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if Users.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if Users.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class ImageListSerializer(serializers.ModelSerializer):
    images = ImageDataSerializer(many=True, required=False)

    class Meta:
        model = ImageList
        fields = "__all__"

    def create(self, validated_data):
        try:
            # try to get and save images (if any)
            images_data = dict(
                (self.context['request'].FILES).lists()).get('images', None)
            for image in images_data:
                image = ImageData.objects.create(
                    images=image, **validated_data)
            mapped = ImageList.objects.create(
                imageList=images_data, time=uploaded(), **validated_data)
        except:
            # if no images are available - create using default image
            raise Exception("No images found for this request.")
        return mapped


class ResultDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultData
        fields = "__all__"


class SegmentationTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SegmentationTask
        fields = '__all__'


class ReconstructionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconstructionTask
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @ classmethod
    def get_token(cls, Users):
        token = super().get_token(Users)

        # Add custom claims
        token["userid"] = Users.id
        token['username'] = Users.username

        return token
