# Generated by Django 4.0 on 2022-01-23 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_productfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
