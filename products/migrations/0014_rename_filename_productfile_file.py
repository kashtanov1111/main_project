# Generated by Django 4.0 on 2022-01-23 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_productfile_filename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productfile',
            old_name='filename',
            new_name='file',
        ),
    ]
