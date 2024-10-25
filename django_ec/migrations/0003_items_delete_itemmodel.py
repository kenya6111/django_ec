# Generated by Django 4.2.16 on 2024-10-25 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ec', '0002_remove_itemmodel_author_remove_itemmodel_readtext'),
    ]

    operations = [
        migrations.CreateModel(
            name='items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('star', models.IntegerField(blank=True, default=1, null=True)),
                ('price', models.IntegerField(blank=True, default=1, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('is_sale', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='ItemModel',
        ),
    ]
