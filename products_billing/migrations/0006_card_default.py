# Generated by Django 4.0 on 2022-01-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_billing', '0005_delete_cardmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]
