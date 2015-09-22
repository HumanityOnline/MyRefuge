# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0005_auto_20150922_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizenspace',
            name='country',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
