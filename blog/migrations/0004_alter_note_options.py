# Generated by Django 3.2.9 on 2021-11-29 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_delete_flavor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-date_time']},
        ),
    ]