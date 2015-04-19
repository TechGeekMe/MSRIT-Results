# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0002_auto_20150419_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='cgpa',
            field=models.CharField(max_length=5),
        ),
    ]
