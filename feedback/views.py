from django.shortcuts import render, redirect
from .models import FeedbackForm, FeedbackCollection, FeedbackData, Placement
from .utils import get_form


def submit_feedback(request, form_id, collection_id=None, placement_id=None):
    form = get_form(form_id)
    collection = form.collect(
        data=request.POST,
        collection_id=collection_id,
        placement_id=placement_id,
        user=request.user)
    if request.POST.get('next'):
        return redirect(request.POST.next)
    else:
        return render(request, 'complete.html', {})
