from django.db import models
from django.conf import settings

from address.models import AddressField
from common.helpers import GENDER
from common.models import UserProfile
from django_countries import countries
from select_multiple_field.models import SelectMultipleField
from userena.models import UserenaSignup

# Create your models here.
class Refugee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(
        max_length=1000,
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    current_address = AddressField()
    dob = models.DateField()
    hometown = models.CharField(
        max_length=255,
    )
    story = models.TextField()
    countries = SelectMultipleField(
        max_length=1000,
        choices=tuple(countries),
    )

class FamilyMember(models.Model):
    name = models.CharField(max_length=1000)
    dob = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    relationship = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='family_photos')
    refugee = models.ForeignKey(Refugee)
