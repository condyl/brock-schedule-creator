from django.shortcuts import render,redirect
from . import models
import csv

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def upload(request):
    return render(request, 'upload.html')

def import_csv_to_database(request):
    context = {}

    if len(request.FILES) != 0:
        file = request.FILES['file'] 
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            print(row)
            course = models.Course()
            course.course_name = row['course_name']
            course.course_code = row['course_code']
            course.course_type = row['course_type']
            course.course_days = row['course_days']
            course.course_start_time = row['course_start_time']
            course.course_end_time = row['course_end_time']
            if row['course_start_date'] == "0000-00-00": 
                course.course_start_date = "2024-04-29"
                course.course_end_date = "2024-07-12"
            else:
                course.course_start_date = row['course_start_date']
                course.course_end_date = row['course_end_date']
            course.course_instructor = row['course_instructor']
            course.course_term = "spring"
            course.course_year = "2024"
            course.save()

    else:
        return redirect("upload")
        


    return render(request, 'import_csv_to_database.html')