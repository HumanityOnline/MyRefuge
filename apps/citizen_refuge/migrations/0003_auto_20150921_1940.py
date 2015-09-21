# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import address.models
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0002_auto_20150920_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizenrefuge',
            name='address',
            field=address.models.AddressField(default=b'', to='address.Address'),
        ),
        migrations.AlterField(
            model_name='citizenspace',
            name='additional',
            field=select_multiple_field.models.SelectMultipleField(max_length=4, choices=[(b'1', b'wifi available'), (b'2', b'provide free food'), (b'3', b'share advice about the city and its services'), (b'4', b'hang out with the refugees')]),
        ),
    ]
