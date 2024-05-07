from django.db import models

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=10)
    course_type = models.CharField(max_length=10)
    course_days = models.CharField(max_length=10)
    course_start_time = models.TimeField()
    course_end_time = models.TimeField()
    course_start_date = models.DateField()
    course_end_date = models.DateField()
    course_instructor = models.CharField(max_length=100)