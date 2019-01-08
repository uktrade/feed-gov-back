from django.shortcuts import render
from feedback.models import FeedbackForm

# Create your views here.
def main_view(request):
    form = FeedbackForm.objects.first()
    return render(request, 'index.html', {'form': form})


def dict_view(request):
    form = FeedbackForm.objects.first()
    return render(request, 'index.html', {'form': form.to_dict()})


def key_view(request):
    return render(request, 'index.html', {'form': 'FORM_ONE'})