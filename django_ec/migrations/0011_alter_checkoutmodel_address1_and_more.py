# Generated by Django 4.2.16 on 2024-11-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0010_checkoutmodel_credit_number_alter_checkoutmodel_cvv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutmodel',
            name='address1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='credit_expiration',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='cvv',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='name_on_card',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='user_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkoutmodel',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
