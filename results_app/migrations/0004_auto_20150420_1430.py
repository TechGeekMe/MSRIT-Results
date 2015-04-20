# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0003_auto_20150419_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='cgpa',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='result',
            name='sgpa',
            field=models.FloatField(),
        ),
    ]
