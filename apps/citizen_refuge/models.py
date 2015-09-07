from django.conf import settings
from django.db import models

from address.models import AddressField
from common.helpers import APPLICATION_STATUS, CITIZEN_REFUGE_ADDITIONAL, GENDER, UniqueMediaPath
from refugee.models import Refugee
from select_multiple_field.models import SelectMultipleField


class CitizenRefuge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    address = AddressField()
    short_description = models.CharField(max_length=255)

    num_beds = models.IntegerField(default=0)
    long_description = models.TextField()
    wifi = models.NullBooleanField(
        blank=True,
    )


class DateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    citizen = models.ForeignKey(CitizenRefuge)


class Application(models.Model):
    refugee = models.OneToOneField(Refugee)
    citizen = models.OneToOneField(CitizenRefuge)
    status = models.CharField(
        max_length=1,
        choices=APPLICATION_STATUS,
    )
