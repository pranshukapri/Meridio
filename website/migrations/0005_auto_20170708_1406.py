# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-08 14:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20170708_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedobjects',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2017, 7, 8, 14, 6, 59, 387412, tzinfo=utc)),
        ),
    ]
