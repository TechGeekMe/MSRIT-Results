# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usn', models.CharField(max_length=15)),
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
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('student', models.OneToOneField(primary_key=True, serialize=False, to='results_app.Student')),
                ('credits_registered', models.IntegerField()),
                ('credits_earned', models.IntegerField()),
                ('sgpa', models.FloatField()),
                ('cgpa', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='result',
            field=models.ForeignKey(to='results_app.Result'),
        ),
    ]
