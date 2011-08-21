from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User)
    address_1 = models.CharField(_('Address 1'), max_length=64)
    address_2 = models.CharField(_('Address 1'), max_length=64, blank=True)
    address_3 = models.CharField(_('Address 1'), max_length=64, blank=True)
    address_4 = models.CharField(_('Address 1'), max_length=64, blank=True)
    country = models.CharField(_('Country'), max_length=64)
    phone = models.CharField(_('Phone Number'), max_length=64, blank=True)
    afn = models.CharField(_('Ancestral File Number'), max_length=30, blank=True)

