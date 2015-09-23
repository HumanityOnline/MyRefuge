# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umessages', '__first__'),
        ('citizen_refuge', '0007_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='umessages.Message')),
                ('application', models.ForeignKey(to='citizen_refuge.Application')),
            ],
            bases=('umessages.message',),
        ),
    ]
