import uuid
from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from .base import BaseFeedbackModel
from .exceptions import InvalidElementOption


class FeedbackForm(BaseFeedbackModel):
    """
    The Form is the top level root in a feedback process. It is a collection
    of fields and content to retrieve a full feedback form.
    Forms can be identified by their unique id or unique humanised key
    """
    name = models.CharField(max_length=250, null=False, blank=False)
    key = models.CharField(max_length=32, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.key:
            return f'{self.name} [{self.key}]'
        return f'{self.name}'

    def _to_dict(self):
        return {
            'name': self.name,
            'key': self.key,
            'description': self.description,
            'elements': [
                element.to_dict() for element in self.formelement_set.all().order_by('order')
            ]
        }

    @property
    def num_of_elements(self):
        return self.formelement_set.all().count()


class ElementType(models.Model):
    """
    The type of input fields available.
    A field type can specify a set of options with defaults which will be used
    in the rendering of the element
    """
    name = models.CharField(max_length=250, null=False, blank=False)
    key = models.CharField(max_length=30, null=False, blank=False)
    options = fields.JSONField(default=dict)

    def __str__(self):
        return self.name


class FormElement(BaseFeedbackModel):
    """
    An element in a form, with a specified type.
    There are 3 descriptive fields, name, label and description, as well as
    an optional options to specify custom options for the element.
    Elements are ordered in a form via the order field
    """
    form = models.ForeignKey(FeedbackForm, null=False, blank=False, on_delete=models.PROTECT)
    element_type = models.ForeignKey(ElementType, null=False, blank=False, on_delete=models.PROTECT)
    name = models.CharField(max_length=250, null=False, blank=False)
    label = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    options = fields.JSONField(default=dict, blank=True)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.element_type}: {self.name}'

    def _to_dict(self):
        return {
            'type': self.element_type.name,
            'label': self.label,
            'description': self.description,
            'order': self.order,
            'options': self.options or self.element_type.options,

        }

    def validate_options(self, options):
        """
        Validate the all given option keys are actually valid options based on the element
        type. Raise InvalidElementOption exception if not.
        """
        for key in options:
            if key not in self.element_type.options:
                raise InvalidElementOption(f'{key} is not a valid option for {self.element_type}')
        return True

    def set_options(self, options):
        """
        For a given set of element options, validate them and overlay any on top of of the
        element type default
        """
        self.validate_options(options)
        _options = self.element_type.options
        for key in options:
            _options[key] = type(_options[key])(options[key])
        self.options = _options


class FeedbackData(BaseFeedbackModel):
    """
    Data captured for an element in a form, by a user (optional).
    Data is kept as a JSON field so it can be a simple value (string or boolean) or a more
    complex one
    """
    element = models.ForeignKey(FormElement, null=False, blank=False, on_delete=models.PROTECT)
    value = fields.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(getattr(settings, 'FEEDBACK_USER_MODEL'), null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        _str = f'{self.element.form} -> {self.element} -> {self.value}'
        if self.created_by:
            _str = f'{_str} ({self.created_by})'
        return _str
