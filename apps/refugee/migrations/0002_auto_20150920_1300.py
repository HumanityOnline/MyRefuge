# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import address.models


class Migration(migrations.Migration):

    dependencies = [
        ('refugee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='refugee',
            name='full_address',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='refugee',
            name='current_address',
            field=address.models.AddressField(blank=True, to='address.Address', null=True),
        ),
        migrations.AlterField(
            model_name='refugee',
            name='story',
            field=models.TextField(blank=True),
        ),
    ]
