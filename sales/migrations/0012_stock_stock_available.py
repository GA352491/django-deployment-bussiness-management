# Generated by Django 3.0.6 on 2020-05-26 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_invoice_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='stock_available',
            field=models.FloatField(null=True),
        ),
    ]
