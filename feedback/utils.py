"""
Utility functions.
"""
from uuid import UUID
from functools import singledispatch
from .models import FeedbackForm


@singledispatch
def get_form(form):
    return form


@get_form.register(UUID)
def _(form):  # noqa
    return FeedbackForm.objects.get(id=form)


@get_form.register(str)
def _(form):  # noqa
    return FeedbackForm.objects.by_key(form)


def is_uuid(value):
    """
    Validate a value to be or not to be a UUID4
    """
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False
