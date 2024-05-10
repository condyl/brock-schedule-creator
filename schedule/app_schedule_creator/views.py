from django.shortcuts import render,redirect
from . import models
import csv
from .schedule import get_course_options

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def schedule(request):
    context={}
    semester = request.POST.get('semester')
    courses_str = request.POST.get('courses')
    courses = courses_str.split(',')
    for i in range(len(courses)):
        courses[i] = courses[i].strip()
    #print(courses)
    valid_course_options = get_course_options(courses, semester, 2024)
    for choice in valid_course_options:
        for courses in choice:
        #print(option)
            for course in courses:
                print(course.course_name, course.course_type, course.course_days, course.course_start_time, course.course_end_time, course.course_instructor)
        print()
    
    #print(course_options)

    return render(request, 'schedule.html', context=context)

def upload(request):
    return render(request, 'upload.html')

def import_csv_to_database(request):
    if len(request.FILES) != 0:
        file = request.FILES['file'] 
        #uploaded_file = models.Upload()
        #uploaded_file.upload_file = file
        #uploaded_file.save()

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
        
    uploaded_file = models.Upload()
    uploaded_file.upload_file = request.FILES['file']
    uploaded_file.save()

    return render(request, 'import_csv_to_database.html')