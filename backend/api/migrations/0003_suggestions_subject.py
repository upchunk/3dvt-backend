# Generated by Django 4.1.2 on 2022-10-27 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_suggestions"),
    ]

    operations = [
        migrations.AddField(
            model_name="suggestions",
            name="subject",
            field=models.CharField(
                help_text="Suggestions's Subject", max_length=50, null=True
            ),
        ),
    ]