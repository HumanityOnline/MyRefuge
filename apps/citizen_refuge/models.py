from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos

from select_multiple_field.models import SelectMultipleField
from address.models import AddressField

from common.helpers import APPLICATION_STATUS, CITIZEN_SPACE_ADDITIONAL, GENDER, UniqueMediaPath
from common.geo import address_to_location, location_to_latlon, location_to_city
from refugee.models import Refugee


class CitizenRefuge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    address = AddressField(default="")

    def __repr__(self):
        return '<CitizenRefuge(pk={pk}, user={user})>'.format(pk=self.pk, user=self.user)

    def __unicode__(self):
        return self.__repr__()


class CitizenSpaceManager(gis_models.GeoManager):

    # TODO(hoatle): implement this
    # this could help: http://www.rkblog.rk.edu.pl/w/p/shops-near-you-geographic-features-geodjango/
    # sort by distance
    def search(self, address, date_range, guests, **kwargs):
        """Search spaces basing on the address, date_range, guests, etc"""
        location = address_to_location(address)
        address_lat, address_lon = location_to_latlon(location)
        city = location_to_city(location)
        current_point = geos.fromstr('POINT(%s %s)' % (address_lon, address_lat))

        pass


class CitizenSpace(models.Model):
    headline = models.CharField(max_length=255)
    full_description = models.TextField()
    address = AddressField()
    # auto set from address field
    city = models.CharField(max_length=255, blank=True, null=True)
    guests = models.IntegerField(default=0)  # number of guests to be accommodated
    additional = SelectMultipleField(max_length=4, choices=CITIZEN_SPACE_ADDITIONAL)
    # auto set from address field
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)
    citizen = models.ForeignKey(CitizenRefuge)

    objects = CitizenSpaceManager()

    def save(self, **kwargs):
        # TODO(hoatle): update location only if address is changed
        # https://github.com/smn/django-dirtyfields
        location = address_to_location(self.address.raw)

        lat, lon = location_to_latlon(location)
        point = "POINT(%s %s)" % (lon, lat)
        self.location = geos.fromstr(point)

        city = location_to_city(location)
        self.city = city
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
    status = models.CharField(
        max_length=1,
        choices=APPLICATION_STATUS,
    )
