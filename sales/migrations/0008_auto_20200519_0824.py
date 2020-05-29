# Generated by Django 3.0.6 on 2020-05-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_auto_20200519_0818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='tags',
        ),
        migrations.AddField(
            model_name='stock',
            name='tags',
            field=models.ManyToManyField(to='sales.Tag'),
        ),
    ]
