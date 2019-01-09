from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from .base import BaseFeedbackModel
from .exceptions import InvalidElementOption


USER_MODEL_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
DEFAULT_PLACEMENT_KEY = getattr(settings, 'DEFAULT_PLACEMENT_KEY', 'DEFAULT')
ANONYMOUS_COLLECTION = getattr(settings, 'ANONYMOUS_COLLECTION', True)
MANAGED_MODELS = getattr(settings, 'MANAGED_FEEDBACK_MODELS', True)

class PlacementManager(models.Manager):
    def get_placement(self, key=None):
        """
        Always return a placement. If key is not provided it will default to the key defined in DEFAULT_PLACEMENT_KEY setting.
        """
        key = key or DEFAULT_PLACEMENT_KEY
        placement, _ = self.get_or_create(id=key)
        return placement


class Placement(BaseFeedbackModel):
    """
    A placement is a unique location a form can be placed at on a web resource. Placements are used to
    group forms submitted from the same location.
    It is possible to predefine all placements or allow generating those on the fly. Either way,
    a placement must be used when collecting data for a form. If one is not provided,
    a default one will be used (if using the API)
    A placement can be identified via it's unique user defined id. A more friendly descriptive name and url are optional.
    """
    id = models.CharField(max_length=64, null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    objects = PlacementManager()

    class Meta:
        managed = MANAGED_MODELS

    def __str__(self):
        return f'{self.id} [{self.name}]'

    def _to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }


class FeedbackFormManager(models.Manager):
    def by_key(self, key):
        return self.get(key=key)


class FeedbackForm(BaseFeedbackModel):
    """
    The Form is the top level root in a feedback process. It is a collection
    of fields and content to retrieve a full feedback form.
    Forms can be identified by their unique id or an optional unique humanised key
    """
    name = models.CharField(max_length=250, null=False, blank=False)
    key = models.CharField(max_length=32, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)

    objects = FeedbackFormManager()

    class Meta:
        managed = MANAGED_MODELS

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
                element.to_dict() for element in self.elements
            ]
        }

    def add_element(self, element_type, name, label=None, description=None, options=None):
        element = FormElement(
            form=self,
            element_type=element_type,
            name=name,
            label=label,
            description=description
        )
        if options:
            element.set_options(options)
        element.order = self.num_of_elements + 1
        element.save()
        return element

    @property
    def elements(self):
        return self.formelement_set.all().order_by('order')

    @property
    def num_of_elements(self):
        return self.formelement_set.all().count()

    @property
    def collections(self):
        return self.feedbackcollection_set.all().order_by('-created_at')

    def collect(self, data, collection_id=None, placement_id=None, user=None):
        """
        Perform a data collection for this form using a data dict
        """
        if ANONYMOUS_COLLECTION or (user and user.is_anonymous):
            user = None
        collection = FeedbackCollection.objects.get_collection(
            form=self,
            collection_id=collection_id,
            placement_id=placement_id,
            user=user)
        for element in self.elements:
            if str(element.id) in data:
                form_data, _ = FeedbackData.objects.get_or_create(
                    collection=collection,
                    element=element
                )
                form_data.value = element.cast_as_type(data[str(element.id)])
                form_data.save()
        collection.refresh_from_db()
        return collection

    def average_score(self, placement, element):
        """
        Calculate an average score for a placement for this form based on input
        provided in the given element. If the element is not a range, returns None.
        Note, this is currently done in code and not via the ORM/SQL.
        """
        if element.is_range:
            elements = FeedbackData.objects.filter(
                collection__form=self,
                collection__placement=placement,
                element=element,
                value__isnull=False,
            ).values_list('value', flat=True)
            _int_values = [i for i in map(lambda x: int(x) if str(x).isdigit() else None, elements) if i is not None]
            return sum(_int_values) / len(_int_values)
        return None


class ElementType(models.Model):
    """
    The type of input fields available.
    A field type can specify a set of options with defaults which will be used
    in the rendering of the element.

    One convention is followed as far as element type options are concerned:
        - A feedback element is considered a "range" (or scale) element if it has the min/max options.
    """
    name = models.CharField(max_length=250, null=False, blank=False)
    key = models.CharField(max_length=30, null=False, blank=False)
    options = fields.JSONField(default=dict)

    class Meta:
        managed = MANAGED_MODELS

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'key': self.key,
            'options': self.options
        }


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

    class Meta:
        managed = MANAGED_MODELS

    def __str__(self):
        return f'{self.element_type}: {self.name}'

    def _to_dict(self):
        return {
            'element_type': self.element_type.to_dict(),
            'name': self.name,
            'label': self.label,
            'description': self.description,
            'order': self.order,
            'is_range': self.is_range,
            'as_range': list(self.as_range) if self.is_range else None,
            'options': self.get_options(),
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

    def get_options(self):
        _options = self.element_type.options
        if isinstance(_options, dict) and self.options:
            _options.update(self.options)
        return _options

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

    def cast_as_type(self, value):
        """
        If the options dicate a data type of int or str, ensure the value is of tha type
        """
        types = {
            'int': int,
            'str': str,
        }
        options = self.get_options()
        if options.get('type') in types:
            return types[options['type']](value)
        return value

    @property
    def is_range(self):
        """
        An element is a range if it contains a min/max options
        """
        options = self.get_options()
        return ('min' in options and 'max' in options) or bool(options.get('labels'))

    @property
    def as_range(self):
        options = self.get_options()
        if options.get('labels'):
            return options['labels']
        return range(options['min'], options['max'] + 1)


class FeedbackCollectionManager(models.Manager):
    def get_collection(self, form, collection_id=None, placement_id=None, user=None):
        """
        Get an existing collection (to append to it in case of a wizard form scenario)
        or create a new one. If placement is not provided, the default will be used.
        """
        if collection_id:
            return self.get(id=collection_id, form=form)
        return self.create(
            form=form,
            placement=Placement.objects.get_placement(key=placement_id),
            created_by=user
        )

class FeedbackCollection(BaseFeedbackModel):
    """
    A single collection of a feedback form, used to group all collected element data.
    A collection is tied to a placement and an optional user identifier.
    """
    form = models.ForeignKey(FeedbackForm, null=False, blank=False, on_delete=models.PROTECT)
    placement = models.ForeignKey(Placement, null=False, blank=False, on_delete=models.PROTECT)
    created_by = models.ForeignKey(USER_MODEL_PATH, null=True, blank=True, on_delete=models.PROTECT)

    objects = FeedbackCollectionManager()

    class Meta:
        managed = MANAGED_MODELS

    def __str__(self):
        return f'{self.form} @ {self.placement} [{self.created_at}]'

    @property
    def data(self):
        return self.feedbackdata_set.all().order_by('element__order')

    def _to_dict(self):
        _dict = {
            'placement': self.placement.to_dict(),
            'created_by': str(self.created_by.pk) if self.created_by else None,
            'data': [
                item.to_dict() for item in self.data
            ]
        }
        return _dict


class FeedbackData(BaseFeedbackModel):
    """
    Data captured for an element in a form, by a user (optional).
    Data is kept as a JSON field so it can be a simple value (string or boolean) or a more
    complex one
    """
    collection = models.ForeignKey(FeedbackCollection, null=False, blank=False, on_delete=models.PROTECT)
    element = models.ForeignKey(FormElement, null=False, blank=False, on_delete=models.PROTECT)
    value = fields.JSONField(null=True, blank=True)

    class Meta:
        managed = MANAGED_MODELS

    def __str__(self):
        _str = f'{self.element.form} -> {self.element} -> {self.value}'
        return _str

    def _to_dict(self):
        return {
            'id': str(self.id),
            'element': self.element.to_dict(),
            'value': self.value,
        }
