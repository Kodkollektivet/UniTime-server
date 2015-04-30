# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(max_length=10)),
                ('course_anmalningskod', models.CharField(max_length=10, blank=True)),
                ('season', models.CharField(max_length=2)),
                ('html_url', models.CharField(max_length=254)),
                ('year', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('start_time', models.CharField(max_length=20)),
                ('stop_time', models.CharField(max_length=20)),
                ('info', models.TextField(blank=True)),
                ('room', models.CharField(max_length=20, blank=True)),
                ('group', models.CharField(max_length=100, blank=True)),
                ('course', models.ForeignKey(to='timeedit.Course')),
            ],
        ),
    ]
