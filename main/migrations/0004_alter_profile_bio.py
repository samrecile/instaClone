# Generated by Django 4.0 on 2021-12-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_profile_first_name_remove_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=350),
        ),
    ]