
from django.core.mail import EmailMultiAlternatives
from .models import (Ngo)
import logging

from common.geo import (address_to_location, location_to_latlon, location_to_city,
                        location_to_country)
from django.contrib.gis import geos, measure

class NgoUtils(object):

    @staticmethod
    def SendEmail(space_id, ngoEmail):
        email_msg = NgoUtils.createMsg(space_id)
        ngoEmail = ["Nathan", "nathan@eit.co.nz"]
        try:
            msg = EmailMultiAlternatives(subject="MyRefuge new room avaliable near", body=email_msg,
                                         from_email="help@myrefuge.world", to=ngoEmail)
            response = msg.send()
            #response = msg.mandrill_response()
            if response is None:
                logging.info("Error while sending an email")
            else:
                logging.info('Success while sending')
        except Exception as e:
            raise

    @staticmethod
    def findNGOs(spaceAddress, spaceId):
        latitude_range = 0.8
        longitude_range = 0.8

        if spaceAddress.raw:
            location = address_to_location(spaceAddress.raw)
        else:
            location = address_to_location(spaceAddress)

        spaceLat, spaceLng = location_to_latlon(location)

        latituderange=(spaceLat - latitude_range, spaceLat + latitude_range)
        longituderange=(spaceLng - longitude_range, spaceLng + longitude_range)

        query = Ngo.objects.all().filter()

        distance = 100
        current_point = geos.fromstr('POINT(%s %s)' % (spaceLng, spaceLat))
        distance_from_point = {'m': distance}
        query = query.filter(location__distance_lte=(current_point,
                                                     measure.D(**distance_from_point)))
        ngos = query.distance(current_point).order_by('distance')
        #.order_by('distance')
        #ngos = Ngo.objects.filter(latitude__range=latituderange, longitude__range=longituderange)

        for ngo in ngos:
            NgoUtils.SendEmail(spaceId, ngo.email)

    @staticmethod
    def createMsg(spaceId):
        msg = "Dear [Charity name]\n\n" \
              "MyRefuge is an AirBnB service that allows refugees to find and request hosting from people opening up their homes. We understand that [charity name] supports this process as well.\n\n" \
              "[Name of person] in [Name of neighbourhood, city] has decided to share their home with refugees. Here's a link to their offer [link to property].\n\n" \
              "We hope you find this useful in finding hosts e.g. for legal destitute asylums and those those who have been successful in Asylum Application but are not yet receiving state housing support.\n\n" \
              "If you have any questions about MyRefuge see http://myrefuge.world/help/ or get in touch with sholi@humanityonline.org \n\n" \
              "Best wishes, \n" \
              "Sholi".format(
            spaceId)
        return msg
