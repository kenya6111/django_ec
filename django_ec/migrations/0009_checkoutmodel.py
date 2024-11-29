# Generated by Django 4.2.16 on 2024-11-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0008_remove_cartmodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckoutModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('name_on_card', models.CharField(max_length=100)),
                ('credit_expiration', models.CharField(max_length=10)),
                ('cvv', models.PositiveSmallIntegerField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
