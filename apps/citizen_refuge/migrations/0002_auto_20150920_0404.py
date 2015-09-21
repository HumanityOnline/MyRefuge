# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import address.models
import select_multiple_field.models
import common.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('citizen_refuge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitizenSpace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=255)),
                ('full_description', models.TextField()),
                ('guests', models.IntegerField(default=0)),
                ('additional', select_multiple_field.models.SelectMultipleField(max_length=4, choices=[(1, b'wifi available'), (2, b'provide free food'), (3, b'share advice about the city and its services'), (4, b'hang out with the refugees')])),
                ('address', address.models.AddressField(to='address.Address')),
            ],
        ),
        migrations.CreateModel(
            name='SpacePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=common.helpers.UniqueMediaPath(b'space_photos'))),
                ('space', models.ForeignKey(to='citizen_refuge.CitizenSpace')),
            ],
        ),
        migrations.RemoveField(
            model_name='application',
            name='citizen',
        ),
        migrations.RemoveField(
            model_name='citizenrefuge',
            name='long_description',
        ),
        migrations.RemoveField(
            model_name='citizenrefuge',
            name='num_beds',
        ),
        migrations.RemoveField(
            model_name='citizenrefuge',
            name='short_description',
        ),
        migrations.RemoveField(
            model_name='citizenrefuge',
            name='wifi',
        ),
        migrations.RemoveField(
            model_name='daterange',
            name='citizen',
        ),
        migrations.AddField(
            model_name='citizenspace',
            name='citizen',
            field=models.ForeignKey(to='citizen_refuge.CitizenRefuge'),
        ),
        migrations.AddField(
            model_name='application',
            name='space',
            field=models.OneToOneField(default='', to='citizen_refuge.CitizenSpace'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='daterange',
            name='space',
            field=models.ForeignKey(default='', to='citizen_refuge.CitizenSpace'),
            preserve_default=False,
        ),
    ]
