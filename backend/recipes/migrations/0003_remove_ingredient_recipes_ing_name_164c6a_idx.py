# Generated by Django 4.2.3 on 2023-07-12 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='ingredient',
            name='recipes_ing_name_164c6a_idx',
        ),
    ]
