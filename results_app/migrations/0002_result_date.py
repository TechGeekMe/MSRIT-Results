# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='date',
            field=models.DateField(default=datetime.date(2015, 6, 1)),
            preserve_default=False,
        ),
    ]
