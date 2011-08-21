from django.db import models
from django.utils.translation import ugettext_lazy as _

class Person(models.Model):
    MALE, FEMALE, UNKNOWN = ('m', 'f', 'u')

    GENDERS = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (UNKNOWN, _('Unknown')),
    )

    given_names = models.CharField(_('Given Names'), max_length=200)
    surname = models.CharField(_('Surname'), max_length=64)
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDERS, default=UNKNOWN)
    title = models.CharField(_('Title'), max_length=20, blank=True)
    married_name = models.CharField(_('Married Name'), max_length=64, blank=True)
    also_known_as = models.CharField(_('Also Known As'), max_length=64, blank=True)
    nickname = models.CharField(_('Nickname'), max_length=64, blank=True)
    afn = models.CharField(_('Ancestral File Number'), max_length=64, blank=True)
    children = models.ManyToManyField('self', name=_('Children'), related_name='parents', symmetrical=False)

    def __unicode__(self):
        return u'%s /%s/' % (self.given_names, self.surname)

    @property
    def father(self):
        """Returns this person's father, if known"""

        if not hasattr(self, '_father'):
            try:
                self._father = self.parents.get(gender=Person.MALE)
            except Person.DoesNotExist:
                self._father = None

        return self._father

    @property
    def mother(self):
        """Returns this person's mother, if known"""

        if not hasattr(self, '_mother'):
            try:
                self._mother = self.parents.get(gender=Person.FEMALE)
            except Person.DoesNotExist:
                self._mother = None

        return self._mother

    @property
    def siblings(self):
        """Returns all children from this person's parents"""

        siblings = set()
        for parent in self.parents.all():
            siblings.update(parent.children.all())

        siblings.remove(self)
        return siblings
