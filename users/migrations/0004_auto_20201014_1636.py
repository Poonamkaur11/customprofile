# Generated by Django 3.1.2 on 2020-10-14 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_experience_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='education',
            options={'ordering': ['uuid']},
        ),
        migrations.AlterModelOptions(
            name='experience',
            options={'ordering': ['uuid']},
        ),
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ['uuid']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['uuid']},
        ),
        migrations.AlterModelOptions(
            name='skills',
            options={'ordering': ['uuid']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['uuid']},
        ),
    ]