from django.db import models
from django.utils.translation import ugettext_lazy as _

class Person(models.Model):
    MALE, FEMALE, UNKNOWN = ('m', 'f', 'u')

    GENDERS = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (UNKNOWN, _('Unknown')),
    )

    father = models.ForeignKey('self', related_name='paternal_children', blank=True, null=True)
    mother = models.ForeignKey('self', related_name='maternal_children', blank=True, null=True)
    given_names = models.CharField(_('Given Names'), max_length=200)
    surname = models.CharField(_('Surname'), max_length=64)
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDERS, default=UNKNOWN)
    title = models.CharField(_('Title'), max_length=20, blank=True)
    married_name = models.CharField(_('Married Name'), max_length=64, blank=True)
    also_known_as = models.CharField(_('Also Known As'), max_length=64, blank=True)
    nickname = models.CharField(_('Nickname'), max_length=64, blank=True)
    afn = models.CharField(_('Ancestral File Number'), max_length=64, blank=True)

    def __unicode__(self):
        return u'%s /%s/' % (self.given_names, self.surname)

    @property
    def children(self):
        if not hasattr(self, '_children'):
            if self.gender == Person.MALE:
                self._children = self.paternal_children.all()
            elif self.gender == Person.FEMALE:
                self._children = self.maternal_children.all()
            else:
                # can unknowns have children? ;)
                self._children = []

        return self._children

    @property
    def siblings(self):
        """Returns all siblings from both parents of this person"""

        if not hasattr(self, '_siblings'):
            self._siblings = set()

            if self.father:
                self._siblings.update(self.father.children)

            if self.mother:
                self._siblings.update(self.mother.children)

            self._siblings = sorted(self._siblings, key=lambda p: p.birth)

        return self._siblings
