from django.db import models
from django.utils.translation import ugettext_lazy as _

from provinia.tree.models import Person

class BaseEvent(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=255)

    class Meta:
        abstract = True

class Event(BaseEvent):
    person = models.ForeignKey(Person, related_name='%(class)s_set')

    class Meta:
        abstract = True

class OneTimeEvent(BaseEvent):
    person = models.OneToOneField(Person)

    class Meta:
        abstract = True

class LDSEvent(OneTimeEvent):
    temple = models.CharField(_('Temple'), max_length=5)

    class Meta:
        abstract = True

class Marriage(Event):
    to = models.ForeignKey(Person, related_name='marriages')
    divorced = models.BooleanField(_('Divorced'), blank=True)

    class Meta:
        ordering = ('date',)

class Birth(OneTimeEvent):
    pass

class Christening(OneTimeEvent):
    pass

class Death(OneTimeEvent):
    pass

class Burial(OneTimeEvent):
    pass

class Baptism(OneTimeEvent):
    temple = models.CharField(_('Temple'), max_length=5, blank=True)

class Endowment(LDSEvent):
    pass

class SealingToSpouse(Event, LDSEvent):
    pass

class SealingToParents(LDSEvent):
    born_in_covenant = models.BooleanField(_('Born in the Covenant'), blank=True)

