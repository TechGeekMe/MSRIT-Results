# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0003_subjectlist_branch_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectlist',
            name='branch_code',
        ),
        migrations.AddField(
            model_name='subjectlist',
            name='first_year',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
