"""
Template tag to render a whole feedback form based on it's key or id
Usage:
    {% feedback_form key %}

"""
from django.utils.safestring import mark_safe
from django.template import loader
from . import register
from ..models import FeedbackForm
from ..utils import is_uuid


@register.simple_tag
def feedback_form(key):
    kwarg_key = 'id' if is_uuid(key) else 'key'
    form = FeedbackForm.objects.get(**{kwarg_key: key})
    context = {
        'form': form
    }
    template = loader.get_template(f'feedback_form.html')
    return mark_safe(template.render(context))
