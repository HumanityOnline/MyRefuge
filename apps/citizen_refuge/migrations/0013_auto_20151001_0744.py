# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0012_launch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
