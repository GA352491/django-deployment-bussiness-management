# Generated by Django 3.0.6 on 2020-05-19 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_auto_20200519_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out of delivery', 'Out of delivery'), ('Delivered', 'Delivered')], max_length=100, null=True),
        ),
    ]
