# Generated by Django 3.1.2 on 2020-10-22 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
