# Generated by Django 4.0 on 2021-12-31 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_avatar',
        ),
    ]
