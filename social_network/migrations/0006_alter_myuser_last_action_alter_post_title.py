# Generated by Django 4.0.2 on 2022-02-10 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0005_alter_myuser_last_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='last_action',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 10, 16, 54, 43, 440472)),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='title', max_length=200, verbose_name='post_name'),
        ),
    ]
