# Generated by Django 4.2.16 on 2024-11-24 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0012_checkoutmodel_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutmodel',
            name='cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkout', to='django_ec.cartmodel'),
        ),
        migrations.CreateModel(
            name='PurchaseDetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_details', to='django_ec.checkoutmodel')),
            ],
        ),
    ]
