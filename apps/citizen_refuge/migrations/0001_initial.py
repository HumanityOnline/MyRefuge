# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import address.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refugee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, choices=[(b'P', b'Pending'), (b'D', b'Denied'), (b'A', b'Accepted')])),
            ],
        ),
        migrations.CreateModel(
            name='CitizenRefuge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=1, choices=[(b'', b'Gender'), (b'M', b'Male'), (b'F', b'Female'), (b'U', b'Prefer not to say')])),
                ('short_description', models.CharField(max_length=255)),
                ('num_beds', models.IntegerField(default=0)),
                ('long_description', models.TextField()),
                ('wifi', models.NullBooleanField()),
                ('address', address.models.AddressField(to='address.Address')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DateRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('citizen', models.ForeignKey(to='citizen_refuge.CitizenRefuge')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='citizen',
            field=models.OneToOneField(to='citizen_refuge.CitizenRefuge'),
        ),
        migrations.AddField(
            model_name='application',
            name='refugee',
            field=models.OneToOneField(to='refugee.Refugee'),
        ),
    ]
