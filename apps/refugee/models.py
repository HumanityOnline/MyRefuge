from django.db import models
from django.conf import settings

from address.models import AddressField
from common.helpers import GENDER, UniqueMediaPath
from common.models import UserProfile
from django_countries import countries
from select_multiple_field.models import SelectMultipleField
from userena.models import UserenaSignup

# Create your models here.
class Refugee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    current_address = AddressField(blank=True, null=True)
    dob = models.DateField()
    hometown = models.CharField(
        max_length=255,
    )
    full_address = models.CharField(
        max_length=500,
        default=""
    )
    story = models.TextField(blank=True)
    countries = SelectMultipleField(
        max_length=1000,
        choices=tuple(countries),
    )

    def __repr__(self):
        return '<Refugee(pk={pk}, user={user})>'.format(pk=self.pk, user=self.user)

    def __unicode__(self):
        return self.__repr__()

class FamilyMember(models.Model):
    name = models.CharField(max_length=1000)
    dob = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    relationship = models.CharField(max_length=255)
    image = models.ImageField(upload_to=UniqueMediaPath('family_photos'))
    refugee = models.ForeignKey(Refugee)
