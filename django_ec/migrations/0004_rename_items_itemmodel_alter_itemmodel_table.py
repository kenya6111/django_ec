# Generated by Django 4.2.16 on 2024-10-27 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0003_items_delete_itemmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='items',
            new_name='ItemModel',
        ),
        migrations.AlterModelTable(
            name='itemmodel',
            table='items',
        ),
    ]
