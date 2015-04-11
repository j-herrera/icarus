# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ISStrace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issposition',
            name='lon',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='issposition',
            name='lat',
            field=models.FloatField(default=0),
        ),
    ]
