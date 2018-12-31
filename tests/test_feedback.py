from django.test import TestCase
from feedback.models import FeedbackForm, FormElement, ElementType, FeedbackData


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


class FeedbackCreateTest(FeedbackBaseTest):
    def test_creation(self):
        assert self.form.num_of_elements is 2
        assert self.form.elements[0].options['max'] is 10
