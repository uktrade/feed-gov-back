"""
Utility functions.
"""
from uuid import UUID
from functools import singledispatch
from .models import FeedbackForm, Placement



class dotdict(dict):
    """
    dot.access to dict attributes, even across nested dictionaries.
    """
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, key):
        _val = self.get(key)
        if isinstance(_val, dict):
            return dotdict(_val)
        elif isinstance(_val, list):
            return list(map(lambda x: dotdict(x) if isinstance(x, dict) else x, _val))
        return self.get(key)


@singledispatch
def get_form(form):
    return form


@get_form.register(dict)
def _(form):  # noqa
    return dotdict(form)


@get_form.register(UUID)
def _(form):  # noqa
    return FeedbackForm.objects.get(id=form)


@get_form.register(str)
def _(form):  # noqa
    return FeedbackForm.objects.by_key(form)


@singledispatch
def get_placement(placement):
    return placement


@get_placement.register(str)
def _(placement):  # noqa
    return Placement.objects.get(id=placement)


def is_uuid(value):
    """
    Validate a value to be or not to be a UUID4
    """
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False
