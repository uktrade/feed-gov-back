from rest_framework.views import APIView
from rest_framework import status
from feedback.models import (
    FeedbackForm,
    FormElement,
    FeedbackForm,
)
from feedback.exceptions import InvalidElementOption
from .exceptions import (
    NotFoundApiExceptions,
    InvalidRequestParams,
)
from .base import ResponseSuccess


class FeedbackFormApi(APIView):
    def get(self, request, form_id=None, *args, **kwargs):
        order_by = request.query_params.get('order', 'created_at')
        if form_id:
            try:
                form = FeedbackForm.objects.get(id=form_id)
                return ResponseSuccess({
                    'result': form.to_dict()
                })
            except FeedbackForm.DoesNotExist:
                raise NotFoundApiExceptions('Form not found')
        else:
            forms = FeedbackForm.objects.all().order_by(order_by)
            return ResponseSuccess({
                'results': [
                    form.to_dict() for form in forms
                ]
            })

    def post(self, request, form_id=None, *args, **kwargs):
        if form_id:
            try:
                form = FeedbackForm.objects.get(id=form_id)
            except FeedbackForm.DoesNotExist:
                raise NotFoundApiExceptions('Form not found')
        else:
            form = FeedbackForm()
        form.name = request.data.get('name')
        form.key = request.data.get('key')
        form.description = request.data.get('description')
        form.save()
        return ResponseSuccess({
            'result': form.to_dict()
        }, http_status=status.HTTP_201_CREATED)


class FeedbackFormElementApi(APIView):
    def get(self, request, form_id, element_id=None, *args, **kwargs):
        try:
            form = FeedbackForm.objects.get(id=form_id)
        except FeedbackForm.DoesNotExist:
            raise NotFoundApiExceptions('Form not found')
        if element_id:
            try:
                element = FormElement.objects.get(id=element_id, form=form)
                return ResponseSuccess({
                    'result': element.to_dict()
                })
            except FormElement.DoesNotExist:
                raise NotFoundApiExceptions('Element not found')
        else:
            elements = FormElement.objects.filter(form=form).order_by('order')
            return ResponseSuccess({
                'results': [
                    element.to_dict() for element in elements
                ]
            })

    def post(self, request, form_id, element_id=None, *args, **kwargs):
        try:
            form = FeedbackForm.objects.get(id=form_id)
        except FeedbackForm.DoesNotExist:
            raise NotFoundApiExceptions('Form not found')
        if element_id:
            try:
                element = FormElement.objects.get(id=element_id, form=form)
            except FormElement.DoesNotExist:
                raise NotFoundApiExceptions('Element not found')
        else:
            element = FormElement(form=form)
        element.order = request.data.get('order') or form.num_of_elements + 1
        element.name = request.data.get('name')
        element.label = request.data.get('label')
        element.description = request.data.get('description')
        element.element_type = request.data.get('element_type')
        if request.data.get('options'):
            try:
                element.set_options(request.data['options'])
            except InvalidElementOption as exc:
                raise InvalidRequestParams(str(exc))


