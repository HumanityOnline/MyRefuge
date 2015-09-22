# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0004_auto_20150921_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizenspace',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='citizenspace',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='longitude/latitude', blank=True),
        ),
    ]
