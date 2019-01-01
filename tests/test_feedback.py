from django.test import TestCase
from feedback.models import (
    FeedbackForm,
    FormElement,
    ElementType,
    FeedbackData,
    Placement,
    DEFAULT_PLACEMENT_KEY,
)
from .base import FeedbackBaseTest


class FeedbackFormTest(FeedbackBaseTest):
    def test_creation(self):
        self.assertEqual(self.form.num_of_elements, 2)
        self.assertEqual(self.form.elements[0].options['max'], 10)

    def test_default_placement(self):
        placement = Placement.objects.get_placement()
        self.assertEqual(placement.id, DEFAULT_PLACEMENT_KEY)

    def test_options(self):
        element_type = ElementType.objects.get(key='SCALE')
        element = FormElement.objects.get(form=self.form, element_type=element_type)
        self.assertEqual(element.options['max_label'], element_type.options['max_label'])

    def test_collection(self):
        elements = self.form.elements
        data = {
            str(elements[0].id): 3,
            str(elements[1].id): 'notes'
        }
        collection = self.form.collect(data, placement_id='NEW_PAGE')
        data_point_1 = FeedbackData.objects.get(collection=collection, element=elements[0])
        data_point_2 = FeedbackData.objects.get(collection=collection, element=elements[1])
        self.assertEqual(data_point_1.value, 3)
        self.assertEqual(data_point_2.value, 'notes')