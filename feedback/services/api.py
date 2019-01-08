from rest_framework.views import APIView
from rest_framework import status
from feedback.models import (
    FeedbackForm,
    FormElement,
    FeedbackCollection,
)
from feedback.exceptions import InvalidElementOption
from .exceptions import (
    NotFoundApiExceptions,
    InvalidRequestParams,
)
from .base import ResponseSuccess
from ..utils import get_form, is_uuid


class FeedbackFormApi(APIView):
    """
    Get or create feedback forms. Urls are shows relative to the base url.

    ## GET
        `/` Get all forms
        `/<uuid:form_id>/` Get a single form
        `/key/<str:form_key/` Get a single form by key
    """
    def get(self, request, form_id=None, form_key=None, *args, **kwargs):
        order_by = request.query_params.get('order', 'created_at')
        if form_id or form_key:
            try:
                if form_id:
                    form = FeedbackForm.objects.get(id=form_id)
                elif form_key:
                    form = FeedbackForm.objects.get(key=form_key)
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
    """
    Get or create form elements
    """
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


class FeedbackApi(APIView):
    """
    Return feedback collections for a form, data for a single collection, or post new feedback data to it.
    Placement id can be provided in URL or as a query/form param

    ## GET
        feedback/<uuid:form_id>/  Get all collections for this form
        feedback/<uuid:form_id>/collection/<uuid:collection_id>/  Get all data for a single collection
        feedback/<uuid:form_id>/placement/<str:placement_id>/ Get all collections for a specific placment

    ## POST
        feedback/<uuid:form_id>/
        feedback/<uuid:form_id>/placement/<str:placement_id>/
    """
    def get(self, request, form_id, collection_id=None, placement_id=None,  *args, **kwargs):
        placement_id = placement_id or request.query_params.get('placement_id')
        try:
            form = FeedbackForm.objects.get(id=form_id)
            if collection_id:
                collection = FeedbackCollection.objects.get(id=collection_id)
                return ResponseSuccess({
                    'result': collection.to_dict()
                })
            else:
                return ResponseSuccess({
                    'results': [
                        collection.to_dict() for collection in form.collections
                    ]
                })
        except FeedbackForm.DoesNotExist:
            raise NotFoundApiExceptions('Form not found')
        except FeedbackCollection.DoesNotExist:
            raise NotFoundApiExceptions('Collection not found')

    def post(self, request, form_id, collection_id=None, placement_id=None, *args, **kwargs):
        placement_id = placement_id or request.data.get('placement_id')
        form = get_form(form_id)
        collection = form.collect(request.data, collection_id=collection_id, placement_id=placement_id, user=request.user)
        return ResponseSuccess({
            'result': collection.to_dict()
        }, http_status=status.HTTP_201_CREATED)
