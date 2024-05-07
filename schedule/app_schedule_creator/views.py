from django.shortcuts import render
from . import forms

# Create your views here.
def home(request):
    context = {}
    form = forms.CourseForm()
    context['form'] = form
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')