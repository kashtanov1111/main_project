# Generated by Django 3.2.9 on 2021-11-30 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0006_moon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moon',
            name='apollo',
            field=models.DateField(choices=[(datetime.date(1969, 7, 20), 'Apollo 11 (Eagle)'), (datetime.date(1969, 11, 19), 'Apollo 12 (Intrepid)'), (datetime.date(1971, 2, 5), 'Apollo 14 (Antares)'), (datetime.date(1971, 7, 30), 'Apollo 15 (Falcon)'), (datetime.date(1972, 4, 21), 'Apollo 16 (Orion)'), (datetime.date(1972, 12, 11), 'Apollo 17 (Challenger)')], max_length=15),
        ),
    ]
