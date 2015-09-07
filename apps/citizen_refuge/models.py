from django.db import models

from address.models import AddressField
from common.helpers import APPLICATION_STATUS, CITIZEN_REFUGE_ADDITIONAL, GENDER, unique_media_path
from common.models import UserProfile
from refugee.models import Refugee
from select_multiple_field.models import SelectMultipleField

# Create your models here.
class CitizenRefuge(UserProfile):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    address = AddressField()
    num_beds = models.IntegerField()
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    wifi = models.BooleanField()

class Photo(models.Model):
    image = models.ImageField(upload_to=unique_media_path('refuge_photos'))
    citizen_refuge = models.ForeignKey(CitizenRefuge)

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
