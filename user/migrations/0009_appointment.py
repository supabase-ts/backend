# Generated by Django 3.2.20 on 2023-07-28 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_user_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_url', models.TextField(default='')),
                ('start_time', models.DateTimeField()),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advisor', to='user.advisor')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
