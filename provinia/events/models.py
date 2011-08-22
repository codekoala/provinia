from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from provinia.core.utils import subclasses, decamelcase
from provinia.tree.models import Person

class BaseEvent(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=255)

    class Meta:
        abstract = True

    @classmethod
    def get_event_types(cls):
        """
        Finds all subclasses of BaseEvent and returns a dictionary
        """

        if not hasattr(cls, '_subclasses'):
            cls._subclasses = dict(
                (sc, ugettext(decamelcase(sc.__name__)))
                for sc in subclasses(cls)
            )

        return cls._subclasses

class Event(BaseEvent):
    person = models.ForeignKey(Person, related_name='%(class)s_set')

    class Meta:
        abstract = True

    def __unicode__(self):
        return _('for %(person)s') % {'person': self.person}

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

    def __unicode__(self):
        return _('%(person)s to %(to)s') % {'person': self.person, 'to': self.to}

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

class SealingToSpouse(Event):
    temple = models.CharField(_('Temple'), max_length=5)

class SealingToParents(LDSEvent):
    born_in_covenant = models.BooleanField(_('Born in the Covenant'), blank=True)
