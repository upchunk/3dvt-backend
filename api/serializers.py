from dataclasses import fields
from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultData
        fields = "__all__"
