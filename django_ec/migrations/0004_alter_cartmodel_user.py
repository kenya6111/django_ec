# Generated by Django 4.2.16 on 2024-11-11 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_ec', '0003_cartmodel_cartitemmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]