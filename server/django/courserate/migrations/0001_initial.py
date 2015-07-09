# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(max_length=50)),
                ('course_rate', models.FloatField()),
                ('notes', models.TextField()),
                ('ip', models.CharField(max_length=40)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set([('course_code', 'course_rate', 'ip')]),
        ),
    ]
