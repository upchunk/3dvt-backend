# Generated by Django 4.1.2 on 2022-10-14 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0029_landingpage_section_title"),
    ]

    operations = [
        migrations.RenameField(
            model_name="landingpage",
            old_name="section_title",
            new_name="title",
        ),
    ]