from django.shortcuts import render
from feedback.models import FeedbackForm

# Create your views here.
def main_view(request):
    form = FeedbackForm.objects.first()
    return render(request, 'index.html', {'form': form})
