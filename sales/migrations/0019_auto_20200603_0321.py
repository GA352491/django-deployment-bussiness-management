# Generated by Django 3.0.6 on 2020-06-03 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_stock_stock_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
