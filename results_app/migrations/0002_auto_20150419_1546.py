# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='cgpa',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='result',
            name='sgpa',
            field=models.CharField(max_length=5),
        ),
    ]
