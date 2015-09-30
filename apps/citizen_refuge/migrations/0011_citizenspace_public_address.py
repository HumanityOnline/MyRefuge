# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0010_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizenspace',
            name='public_address',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
