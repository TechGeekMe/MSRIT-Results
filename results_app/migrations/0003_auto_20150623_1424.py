# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0002_subjectlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='grade_point',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subjectlist',
            name='subject_name',
            field=models.CharField(max_length=50),
        ),
    ]
