from django.db import models
from django.utils.translation import ugettext_lazy as _

class Person(models.Model):
    GENDERS = (
        ('m', _('Male')),
        ('f', _('Female')),
        ('u', _('Unknown')),
    )

    given_names = models.CharField(_('Given Names'), max_length=200)
    surname = models.CharField(_('Surname'), max_length=64)
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDERS)
    title = models.CharField(_('Title'), max_length=20, blank=True)
    married_name = models.CharField(_('Married Name'), max_length=64, blank=True)
    also_known_as = models.CharField(_('Also Known As'), max_length=64, blank=True)
    nickname = models.CharField(_('Nickname'), max_length=64, blank=True)
    af_number = models.CharField(_('Ancestral File Number'), max_length=64, blank=True)
    children = models.ManyToManyField('self', name=_('Children'), related_name='parents')
