from django import forms
from . import models

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['course_code','course_name','course_type']