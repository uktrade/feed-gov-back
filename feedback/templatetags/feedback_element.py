"""
Template tag to a feedback form element based on it's type.
Usage:
    {% feedback_element element %}

"""
from django.utils.safestring import mark_safe
from django.template import loader
from . import register


@register.simple_tag
def feedback_element(element):
    template_name = element.element_type.key.lower()
    context = {
        'name': element.name,
        'label': element.label,
        'description': element.description,
        'element': element,
    }
    if element.is_range:
        context['range'] = element.as_range
    template = loader.get_template(f'elements/{template_name}.html')
    return mark_safe(template.render(context))
