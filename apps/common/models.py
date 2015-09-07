from django.db import models
from userena.models import UserenaLanguageBaseProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .helpers import GENDER, PROFILE_TYPES, UniqueMediaPath

# Create your models here.
class UserProfile(UserenaLanguageBaseProfile):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='my_profile')

    # Technically this can't be blank,
    # but since no-one can edit it and it's only
    # set in two places we should be OK.
    type = models.CharField(
        max_length=1,
        choices=PROFILE_TYPES,
        null=True,
        blank=True,
    )


class Photo(models.Model):
    image = models.ImageField(upload_to=UniqueMediaPath('gallery'))
    profile = models.ForeignKey(UserProfile)
