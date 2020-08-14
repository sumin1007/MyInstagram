# Generated by Django 3.1 on 2020-08-13 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='c_writer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='c_writer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='writer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='writer', to=settings.AUTH_USER_MODEL),
        ),
    ]
