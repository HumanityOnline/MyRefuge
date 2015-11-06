from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from select_multiple_field.models import SelectMultipleField
from address.models import AddressField
from userena.contrib.umessages.models import Message as BaseMessage

from common.helpers import APPLICATION_STATUS, CITIZEN_SPACE_ADDITIONAL, GENDER, UniqueMediaPath
from common.geo import (address_to_location, location_to_latlon, location_to_city,
                        location_to_country, location_to_public_address, location_to_administrative_area)
from common.mail import send_mass_html_mail
from refugee.models import Refugee

from .managers import CitizenSpaceManager, NGOManager, MessageManager, normalize_name


class CitizenRefuge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    address = AddressField(default="")

    def __repr__(self):
        return '<CitizenRefuge(pk={pk}, user={user})>'.format(pk=self.pk, user=self.user)

    def __unicode__(self):
        return self.__repr__()


class NGO(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    address = AddressField()
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)
    email = models.EmailField(max_length=255)
    other = models.CharField(max_length=255, blank=True, null=True)
    charity_no = models.CharField(max_length=255, blank=True, null=True)
    is_christian_org = models.BooleanField(default=False)

    objects = NGOManager()

    def save(self, **kwargs):
        # TODO(hoatle): update location only if address is changed
        # https://github.com/smn/django-dirtyfields
        location = address_to_location(self.address.raw)
        lat, lon = location_to_latlon(location)
        point = 'POINT(%s %s)' % (lon, lat)
        self.location = geos.fromstr(point)
        super(NGO, self).save()

    def __repr__(self):
        return '<NGO(pk={pk}, name="{name}")>'.format(pk=self.pk, name=self.name)

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


class Launch(models.Model):
    start_date = models.DateTimeField()


def email_ngos(ngos, space):
    """send emails to nearby ngos to a new created space"""
    data_list = []
    email_from = settings.DEFAULT_FROM_EMAIL
    custom_headers = attachments = None
    for ngo in ngos:
        context = {
            'ngo': ngo,
            'space': space,
            'site': Site.objects.get_current(),
            'area': location_to_administrative_area(address_to_location(space.address.raw))
        }

        subject = render_to_string('citizen_refuge/emails/ngo_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        msg_plain = render_to_string('citizen_refuge/emails/ngo_email_message.txt', context)
        msg_html = render_to_string('citizen_refuge/emails/ngo_email_message.html', context)
        data_list.append((subject, msg_plain, msg_html, email_from, [ngo.email], custom_headers, attachments))

    send_mass_html_mail(tuple(data_list))


@receiver(post_save, sender=CitizenSpace)
def notify_nearby_ngos_on_space_created(sender, instance, created, **kwargs):
    if created:
        ngos = NGO.objects.find_nearby(instance)
        email_ngos(ngos, instance)
