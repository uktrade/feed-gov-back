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
