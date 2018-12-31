"""
Template tag to display a two letter badge to denote a case type
Usage:
    {{ case_type_badge case.type }}

"""
from django.utils.safestring import mark_safe
from . import register


@register.simple_tag
def feedback_element(element_type):
    content = f"""<strong>{element_type}</strong>"""
    return mark_safe(content)
