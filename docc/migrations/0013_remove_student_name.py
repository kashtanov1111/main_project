# Generated by Django 3.2.9 on 2021-11-24 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docc', '0012_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
    ]
