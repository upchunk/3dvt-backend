# API Backend by : Habibul Rahman Qalbi

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from backend.settings import AUTHOR_MSG


def upload_to(instance, filename):  # explicitly set upload path and filename
    return "images/{user}/{name}".format(user=instance, name=filename)


def ImageDataset(instance, filename):  # explicitly set upload path and filename
    return "imageData/{user}/{name}".format(user=instance.user.id, name=filename)


def FileDataset(instance, filename):  # explicitly set upload path and filename
    return "fileData/{user}/{name}".format(user=instance.user.id, name=filename)


def MappingDataset(instance, filename):  # explicitly set upload path and filename
    return "mappingData/{user}/{name}".format(user=instance.user.id, name=filename)


def ResultDataset(instance, filename):  # explicitly set upload path and filename
    return "resultData/{user}/{name}".format(user=instance.user.id, name=filename)


class Users(AbstractUser):
    full_name = models.CharField(
        max_length=50, blank=True, null=True, help_text=_("Full Name of the User")
    )
    avatar = models.ImageField(
        upload_to=upload_to, null=True, blank=True, help_text=_("Avatar of this user")
    )
    institution = models.CharField(
        max_length=50, null=True, blank=True, help_text=_("Institution of this user")
    )
    apikey = models.CharField(
        max_length=50,
        null=True,
        help_text=_("User API Key (Token), generated by django AuthToken"),
    )


class Segmentation(models.Model):

    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, help_text=_("Corresponding user ID")
    )
    groupname = models.CharField(
        max_length=50,
        null=True,
        help_text=_("User Group Name for this current Task"),
    )
    status = models.CharField(
        max_length=50,
        null=True,
        help_text=_("Task Status, ex: 'STARTED', 'FINISHED"),
    )
    model = models.CharField(
        max_length=50, null=True, blank=True, help_text=_("Selected Model for the Task")
    )
    createdate = models.DateTimeField(
        auto_now_add=True, help_text=_("Task Creation Date")
    )
    images = models.ManyToManyField(
        "ImageData",
        related_name="image_set",
    )

    class Meta:
        ordering = ["-id"]


class ImageData(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, help_text=_("Corresponding user ID")
    )
    task = models.ForeignKey(
        Segmentation,
        on_delete=models.CASCADE,
        null=True,
        help_text=_("Corresponding Task"),
    )
    images = models.ImageField(
        _("images"),
        upload_to=ImageDataset,
        null=True,
        help_text=_("Image File to be Processed"),
    )
    result = models.ImageField(
        _("result"),
        upload_to=ResultDataset,
        null=True,
        help_text=_("Image Result"),
    )
    uploaded = models.DateTimeField(
        _("Uploaded"),
        auto_now_add=True,
        null=True,
        help_text=_("Image Upload Timeframe"),
    )

    class Meta:
        ordering = ["-id"]


class Reconstruction(models.Model):

    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, help_text=_("Corresponding user ID")
    )
    groupname = models.CharField(
        max_length=50,
        null=True,
        help_text=_("User Group Name for this current Task"),
    )
    status = models.CharField(
        max_length=50,
        null=True,
        help_text=_("Task Status, ex: 'STARTED', 'FINISHED"),
    )
    model = models.CharField(
        max_length=50, null=True, blank=True, help_text=_("Selected Model for the Task")
    )
    createdate = models.DateTimeField(
        auto_now_add=True, help_text=_("Task Creation Date")
    )
    files = models.ManyToManyField(
        "FileData",
        related_name="file_set",
    )

    class Meta:
        ordering = ["-id"]


class FileData(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, help_text=_("Corresponding user ID")
    )
    task = models.ForeignKey(
        Reconstruction,
        on_delete=models.CASCADE,
        null=True,
        help_text=_("Corresponding Task"),
    )
    files = models.FileField(
        _("files"),
        upload_to=FileDataset,
        null=True,
        help_text=_("File to be Processed"),
    )
    uploaded = models.DateTimeField(
        _("Uploaded"),
        auto_now_add=True,
        null=True,
        help_text=_("File Upload Timeframe"),
    )

    class Meta:
        ordering = ["-id"]


class LandingPage(models.Model):
    section = models.CharField(
        _("Section"),
        primary_key=True,
        max_length=50,
        help_text=_("Corresponding Landing Page's Section"),
    )
    title = models.CharField(
        _("title"),
        max_length=50,
        default=str,
        help_text=_("Landing Page's Section Title"),
    )
    content = models.TextField(
        _("Content"),
        null=True,
        help_text=_("Content of Landing Page's Section"),
    )
    image = models.ImageField(
        null=True,
        help_text=_("Optional Image for Landing Page's Section"),
    )
    kwargs = models.JSONField(
        default=dict,
        null=True,
        help_text=_("Optional kwargs for Landing Page's Section"),
    )

    class Meta:
        ordering = ["section"]


class Publication(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50,
        default=str,
        help_text=_("Publication Name / Synopsis"),
    )
    link = models.URLField(_("link"), null=True, help_text=_("Publication Link"))
    description = models.TextField(
        _("Description"),
        null=True,
        help_text=_("Publication Details"),
    )


class Researcher(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50,
        null=True,
        help_text=_("Researcher's Name"),
    )
    avatar = models.ImageField(
        _("Avatar"), null=True, help_text=_("Researcher's Avatar")
    )
    link = models.URLField(
        _("link"), null=True, help_text=_("Researcher's Profile Link on ITS Webiste")
    )
    kwargs = models.JSONField(
        default=dict,
        null=True,
        help_text=_("Optional kwargs for Researcher Section"),
    )


class Suggestions(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, help_text=_("Suggestions's Writer")
    )
    subject = models.CharField(
        max_length=50, null=True, help_text=_("Suggestions's Subject")
    )
    text = models.TextField(null=True, blank=True, help_text=_("Suggestions's Text"))


print(AUTHOR_MSG)
