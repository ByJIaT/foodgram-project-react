# Generated by Django 4.2.3 on 2023-07-15 08:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "ordering": ("first_name", "last_name"),
                "verbose_name": "CustomUser",
                "verbose_name_plural": "CustomUsers",
            },
        ),
    ]
