"""
Template tag to render a whole feedback form based on it's key or id
Usage:
    {% feedback_form key %}

"""
from django.utils.safestring import mark_safe
from django.template import loader
from . import register
from ..utils import get_form


@register.simple_tag
def feedback_form(request, form, placement_id=None):
    form = get_form(form)
    context = {
        'form': form,
        'placement_id': placement_id,
    }
    template = loader.get_template(f'feedback_form.html')
    return mark_safe(template.render(context, request))
