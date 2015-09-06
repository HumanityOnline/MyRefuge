from django.db import models
from userena.models import UserenaLanguageBaseProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .helpers import GENDER

# Create your models here.
class UserProfile(UserenaLanguageBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
