# Generated by Django 4.0.2 on 2022-02-07 19:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='last_action',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 7, 21, 47, 0, 651202)),
        ),
    ]
