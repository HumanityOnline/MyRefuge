# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0008_auto_20150923_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='story',
            field=models.TextField(blank=True),
        ),
    ]
