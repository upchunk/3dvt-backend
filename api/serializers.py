from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group


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
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name', "institusi")

    def validate(self, attrs: dict):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        group, _ = Group.objects.get_or_create(
            name=validated_data["institusi"])
        group.user_set.add(user)
        group.save()

        user.groups.add(group)

        # Save Auto Generated APIKey to Model
        token, _ = Token.objects.get_or_create(user=user)
        user.apikey = str(token.key)
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

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
    email = serializers.EmailField(required=True)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
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
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = "__all__"


class MappingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingData
        fields = "__all__"


class ResultDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultData
        fields = "__all__"


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @ classmethod
    def get_token(cls, Users):
        token = super().get_token(Users)

        # Add custom claims
        token["userid"] = Users.id
        token['username'] = Users.username

        return token
