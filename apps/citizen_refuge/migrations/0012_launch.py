# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0011_citizenspace_public_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Launch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
            ],
        ),
    ]
