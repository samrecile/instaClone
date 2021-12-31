# Generated by Django 4.0 on 2021-12-31 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_user', to='auth.user')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=350)),
                ('profile_pic', models.ImageField(upload_to='ProfilePicture/')),
                ('profile_avatar', models.ImageField(upload_to='AvatarPicture/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='pictsagram/')),
                ('image_caption', models.CharField(max_length=700)),
                ('tag_someone', models.CharField(blank=True, max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('image_likes', models.ManyToManyField(blank=True, default=False, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('imageuploader_profile', models.ForeignKey(blank=True, null='True', on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_post', models.CharField(max_length=150)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to='main.profile')),
                ('commented_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.image')),
            ],
        ),
    ]
