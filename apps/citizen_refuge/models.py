from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos

from select_multiple_field.models import SelectMultipleField
from address.models import AddressField
from userena.contrib.umessages.models import Message as BaseMessage

from common.helpers import APPLICATION_STATUS, CITIZEN_SPACE_ADDITIONAL, GENDER, UniqueMediaPath
from common.geo import (address_to_location, location_to_latlon, location_to_city,
                        location_to_country, location_to_public_address)
from refugee.models import Refugee

from .managers import CitizenSpaceManager, MessageManager, normalize_name


class CitizenRefuge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    address = AddressField(default="")

    def __repr__(self):
        return '<CitizenRefuge(pk={pk}, user={user})>'.format(pk=self.pk, user=self.user)

    def __unicode__(self):
        return self.__repr__()

class CitizenSpace(models.Model):
    headline = models.CharField(max_length=255)
    full_description = models.TextField()
    address = AddressField()
    public_address = models.CharField(max_length=255, blank=True)
    # auto set from address field
    city = models.CharField(max_length=255, blank=True, null=True)
    # auto set from address field
    country = models.CharField(max_length=255, blank=True, null=True)
    guests = models.IntegerField(default=0)  # number of guests to be accommodated

    # auto set from address field
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)

    additional = SelectMultipleField(max_length=10, choices=CITIZEN_SPACE_ADDITIONAL)

    citizen = models.ForeignKey(CitizenRefuge)

    objects = CitizenSpaceManager()

    def save(self, **kwargs):
        # TODO(hoatle): update location only if address is changed
        # https://github.com/smn/django-dirtyfields
        location = address_to_location(self.address.raw)

        self.public_address = location_to_public_address(location)

        lat, lon = location_to_latlon(location)
        point = 'POINT(%s %s)' % (lon, lat)
        self.location = geos.fromstr(point)

        city = location_to_city(location)
        if city is not None:
            # save ascii lower case no white space only
            self.city = normalize_name(city)

        country = location_to_country(location)
        if country is not None:
            # save ascii lower case no white space only
            self.country = normalize_name(country)

        super(CitizenSpace, self).save()

    def __repr__(self):
        return '<CitizenSpace(pk={pk}, headline="{headline}")>'.format(pk=self.pk,
                                                                       headline=self.headline)

    def __unicode__(self):
        return self.__repr__()


class DateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    space = models.ForeignKey(CitizenSpace)


class SpacePhoto(models.Model):
    image = models.ImageField(upload_to=UniqueMediaPath('space_photos'))
    space = models.ForeignKey(CitizenSpace)


class Application(models.Model):
    refugee = models.ForeignKey(Refugee)
    space = models.ForeignKey(CitizenSpace)
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.IntegerField(default=0)
    story = models.TextField(blank=True)
    status = models.CharField(
        max_length=1,
        choices=APPLICATION_STATUS,
        default='P',
    )


class Message(BaseMessage):
    application = models.ForeignKey(Application)

    objects = MessageManager()
