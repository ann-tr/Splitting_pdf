# Generated by Django 5.0.6 on 2024-06-27 05:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project1", "0005_rename_user_pdfinfo_created_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pdfinfo",
            name="created_by",
        ),
    ]