"""
Base class for all tests
"""
from django.test import TestCase
from feedback.models import FeedbackForm, ElementType


class FeedbackBaseTest(TestCase):
    fixtures = ['element_types']

    def setUp(self):
        """
        Setup a form, 2 question elements.
        """
        self.form = FeedbackForm.objects.create(
            name='Test form',
            key='TEST_FORM'
        )
        self.form.add_element(
            element_type=ElementType.objects.get(key='SCALE'),
            name='Satisfaction',
            label='How satisfied are you?',
            description='Select from a scale of 1 to 10',
            options={
                'min': 1,
                'max': 10
            }
        )
        self.form.add_element(
            element_type=ElementType.objects.get(key='TEXTAREA'),
            name='Notes'
        )
