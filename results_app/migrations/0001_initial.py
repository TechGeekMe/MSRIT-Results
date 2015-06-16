# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credits_registered', models.IntegerField()),
                ('credits_earned', models.IntegerField()),
                ('sgpa', models.FloatField()),
                ('cgpa', models.FloatField()),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('usn', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(max_length=15)),
                ('subject_name', models.CharField(max_length=50)),
                ('credits_registered', models.IntegerField()),
                ('credits_earned', models.IntegerField()),
                ('grade', models.CharField(max_length=5)),
                ('result', models.ForeignKey(to='results_app.Result')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='student',
            field=models.ForeignKey(to='results_app.Student'),
        ),
    ]
