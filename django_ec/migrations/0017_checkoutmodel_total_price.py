# Generated by Django 4.2.16 on 2024-11-30 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0016_purchasedetailmodel_item_price_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutmodel',
            name='total_price',
            field=models.BigIntegerField(default=0),
        ),
    ]