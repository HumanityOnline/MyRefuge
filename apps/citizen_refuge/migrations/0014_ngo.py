# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import address.models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('citizen_refuge', '0013_auto_20151001_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='NGO',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='longitude/latitude', blank=True)),
                ('email', models.EmailField(max_length=255)),
                ('other', models.CharField(max_length=255, null=True, blank=True)),
                ('charity_no', models.CharField(max_length=255, null=True, blank=True)),
                ('is_christian_org', models.BooleanField(default=False)),
                ('address', address.models.AddressField(to='address.Address')),
            ],
        ),
    ]
