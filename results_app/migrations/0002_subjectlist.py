# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectList',
            fields=[
                ('course_code', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('subject_name', models.CharField(max_length=15)),
                ('branch_code', models.CharField(max_length=2)),
                ('semester', models.IntegerField()),
            ],
        ),
    ]
