# Generated by Django 3.2.9 on 2021-11-25 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docblog', '0002_dog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docblog.blog'),
        ),
    ]
