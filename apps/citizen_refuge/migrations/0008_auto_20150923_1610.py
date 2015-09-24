# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='guests',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='application',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 23, 16, 10, 45, 383690, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pending'), (b'D', b'Denied'), (b'A', b'Accepted')]),
        ),
    ]
