# Generated by Django 4.0.2 on 2022-02-07 19:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0002_alter_myuser_last_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='last_action',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 7, 21, 49, 35, 270722)),
        ),
    ]