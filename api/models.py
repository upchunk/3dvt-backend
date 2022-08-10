from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_to(instance, filename):  # explicitly set upload path and filename
    return 'images/{filename}'.format(filename=filename)


def ImageDataset(instance, filename):  # explicitly set upload path and filename
    return 'imageData/{filename}'.format(filename=filename)


def MappingDataset(instance, filename):  # explicitly set upload path and filename
    return 'mappingData/{filename}'.format(filename=filename)


def ResultDataset(instance, filename):  # explicitly set upload path and filename
    return 'resultData/{filename}'.format(filename=filename)


class Users(AbstractUser):
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)


class ImageData(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    images = models.FileField(upload_to=ImageDataset, null=True, blank=True)
    mapping = models.FileField(upload_to=MappingDataset, null=True, blank=True)


class ResultData(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    source = models.ForeignKey(ImageData, on_delete=models.CASCADE)
    result_Images = models.FileField(
        upload_to=ResultDataset, null=True, blank=True)
