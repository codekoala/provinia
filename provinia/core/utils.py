import re

DE_CC_RE = re.compile(r'([A-Z][a-z])')

def subclasses(cls, known=None):
    """Attempts to find all subclasses of the specified class"""

    if not isinstance(cls, type):
        raise TypeError(u'cls must be a class, not an instance')

    known = known or []

    for sc in cls.__subclasses__():
        if sc not in known:
            known.append(sc)

            meta = getattr(sc, '_meta', None)
            if meta and getattr(meta, 'abstract'):
                # we don't want abstract classes to appear
                pass
            else:
                yield sc

            for ssc in subclasses(sc, known):
                yield ssc

    raise StopIteration

def decamelcase(string):
    """Turns a CamelCaseWord into Camel Case Word"""

    # TODO: handle acronyms?
    return DE_CC_RE.sub(r' \1', string).strip()
