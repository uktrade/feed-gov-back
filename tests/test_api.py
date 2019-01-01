from unittest.mock import patch
from urllib.parse import urlencode

from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from feedback.services.api import FeedbackFormApi
from .base import FeedbackBaseTest


class FeedbackApiTest(FeedbackBaseTest):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = FeedbackFormApi.as_view()

    def post_form(self, url, payload):
        return self.client.post(
            url, urlencode(payload), content_type="application/x-www-form-urlencoded")

    def get(self, path, params=None):
        response = self.client.get(path, params)
        return response, response.json().get('response')

    def test_forms_get(self):
        response, body = self.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(body['results']), 1)

    def test_form_get(self):
        response, body = self.get(f'/{self.form.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(body['result']['name'], self.form.name)

    def test_form_create(self):
        data = {
            'name': 'Test form 2',
            'description': 'Test desc'
        }
        response = self.post_form('/', data)
        response, body = self.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(body['results']), 2)
        self.assertEqual(body['results'][1]['name'], 'Test form 2')
