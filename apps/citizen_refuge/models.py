from django.conf import settings
from django.db import models

from address.models import AddressField
from common.helpers import APPLICATION_STATUS, CITIZEN_SPACE_ADDITIONAL, GENDER, UniqueMediaPath
from refugee.models import Refugee
from select_multiple_field.models import SelectMultipleField


class CitizenRefuge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    address = AddressField()


class CitizenSpace(models.Model):
    headline = models.CharField(max_length=255)
    full_description = models.TextField()
    address = AddressField()
    guests = models.IntegerField(default=0)  # number of guests to be accommodated
    additional = SelectMultipleField(max_length=4, choices=CITIZEN_SPACE_ADDITIONAL)
    citizen = models.ForeignKey(CitizenRefuge)


class DateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    space = models.ForeignKey(CitizenSpace)


class SpacePhoto(models.Model):
    image = models.ImageField(upload_to=UniqueMediaPath('space_photos'))
    space = models.ForeignKey(CitizenSpace)


class Application(models.Model):
    refugee = models.OneToOneField(Refugee)
    space = models.OneToOneField(CitizenSpace)
    status = models.CharField(
        max_length=1,
        choices=APPLICATION_STATUS,
    )
