# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0003_auto_20150921_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='refugee',
            field=models.ForeignKey(to='refugee.Refugee'),
        ),
        migrations.AlterField(
            model_name='application',
            name='space',
            field=models.ForeignKey(to='citizen_refuge.CitizenSpace'),
        ),
    ]
