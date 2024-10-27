# Generated by Django 4.2.16 on 2024-10-26 01:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0003_items_delete_itemmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
