# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen_refuge', '0013_auto_20151001_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ngo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('location', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(max_digits=9, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=9, decimal_places=6)),
                ('area_working', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('other', models.CharField(max_length=255)),
                ('charity_no', models.CharField(max_length=255)),
                ('is_christian_org', models.BooleanField()),
            ],
        ),
    ]
