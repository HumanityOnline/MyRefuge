from django.db import models

from address.models import AddressField
from common.helpers import APPLICATION_STATUS, CITIZEN_REFUGE_ADDITIONAL
from common.models import UserProfile
from photologue.models import Gallery
from refugee.models import Refugee
from select_multiple_field.models import SelectMultipleField

# Create your models here.
class CitizenRefuge(UserProfile):
    address = AddressField()
    num_beds = models.IntegerField()
    pictures = models.OneToOneField(Gallery)
    additional = SelectMultipleField(
        max_length=10,
        choices=CITIZEN_REFUGE_ADDITIONAL,
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
