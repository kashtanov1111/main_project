# Generated by Django 4.0 on 2022-01-06 09:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doc4', '0007_alter_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(limit_choices_to={'birthday__lte': datetime.date(2004, 1, 6)}, null=True, on_delete=django.db.models.deletion.CASCADE, to='doc4.person'),
        ),
    ]
