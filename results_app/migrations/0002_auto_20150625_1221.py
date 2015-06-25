# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjectlist',
            old_name='branch_code',
            new_name='department_code',
        ),
    ]
