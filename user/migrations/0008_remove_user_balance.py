# Generated by Django 3.2.20 on 2023-07-28 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='balance',
        ),
    ]
