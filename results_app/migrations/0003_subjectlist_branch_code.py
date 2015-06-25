# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0002_auto_20150625_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectlist',
            name='branch_code',
            field=models.CharField(default='CS', max_length=2),
            preserve_default=False,
        ),
    ]
