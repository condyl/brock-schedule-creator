import itertools
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Sends a post request to Brocks site for each unique department that the user registered for.
def fetchBrockData(term, department):
    brockScheduleUrl = 'https://brocku.ca/guides-and-timetables/wp-content/plugins/brocku-plugin-course-tables/ajax.php'
    headers = {
        'Accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    }
    requestData = {
        'action': 'get_programcourses',
        'session': term,
        'type': 'UG',
        'level': 'All',
        'program': department,
        'onlineonly': ''
    }
    response = requests.post(brockScheduleUrl, headers=headers, data=requestData)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, 'html.parser')

# Parses individual course information
def parseCourseData(row, formatted_courses):
    course_code_element = row.find('td', class_='course-code')
    if not course_code_element:
        return None

    course_code = course_code_element.text.strip().replace(" ", "")
    if course_code not in formatted_courses:
        return None

    course_days = row['data-days'].strip()
    course_time = row['data-class_time'].strip()
    course_instructor = row['data-instructor'].strip()
    course_section = row['data-course_section'].strip()
    start_date = datetime.fromtimestamp(int(row['data-startdate'])).strftime('%Y-%m-%d')
    end_date = datetime.fromtimestamp(int(row['data-enddate'])).strftime('%Y-%m-%d')
    course_type = row['data-class_type'].strip()

    try:  # Some courses may not have specific times (I.E Async courses)
        course_start_time, course_end_time = course_time.split('-')
        course_start_time = datetime.strptime(course_start_time.strip(), '%H%M').strftime('%H:%M:%S')
        course_end_time = datetime.strptime(course_end_time.strip(), '%H%M').strftime('%H:%M:%S')
    except:
        course_start_time = ""
        course_end_time = ""

    return {
        'course_code': course_code,
        'course_days': course_days,
        'course_start_time': course_start_time,
        'course_end_time': course_end_time,
        'start_date': start_date,
        'end_date': end_date,
        'course_type': course_type,
        'course_instructor': course_instructor,
        'course_section': course_section
    }

# Parses and organizes course data by department.
def parseDepartmentData(term, department, formatted_courses):
    HTMLParser = fetchBrockData(term, department)
    if not HTMLParser:
        return None

    course_rows = HTMLParser.select('table.course-table tbody tr')
    module_counts = {}

    for row in course_rows:
        course_option = parseCourseData(row, formatted_courses)
        if not course_option:
            continue

        course_type_key = course_option['course_type'][:3]
        if course_type_key not in module_counts:
            module_counts[course_type_key] = []

        module_counts[course_type_key].append(course_option)

    return module_counts

def generateCourseCombos(module_counts):
    return list(itertools.product(*module_counts.values())) if module_counts else []

# Sorts/organizes course options by the day of the week
def sortByDays(courses):
    days = {
        "M": [],
        "T": [],
        "W": [],
        "R": [],
        "F": []
    }
    for course in courses:
        for course_option in course:
            if "M" in course_option['course_days']: days["M"].append(course_option)
            if "T" in course_option['course_days']: days["T"].append(course_option)
            if "W" in course_option['course_days']: days["W"].append(course_option)
            if "R" in course_option['course_days']: days["R"].append(course_option)
            if "F" in course_option['course_days']: days["F"].append(course_option)
    return days

# Checks for valid schedules without overlapping classes
def overlapValidation(days):
    for day in days:
        days[day] = sorted(days[day], key=lambda x: x['course_start_time'])
        for i in range(len(days[day]) - 1):
            if (days[day][i]['course_start_time'] == days[day][i+1]['course_start_time'] or 
                days[day][i]['course_end_time'] == days[day][i+1]['course_end_time']) and \
               (days[day][i]['start_date'] == days[day][i+1]['start_date'] or 
                days[day][i]['end_date'] == days[day][i+1]['end_date']):
                return False
    return True

# generateSchedules() is the main function of schedule.py that coordinates the entire process.
# - Maps term (semester) to appropriate API code.
# - Retrieves and combines course options by department.
# - Filters out invalid schedules with overlapping classes.
def generateSchedules(courses, term):
    term = {"fall": "FW", "winter": "FW", "spring": "SP", "summer": "SU"}.get(term, "FW")
    departments = list(set(course.split()[0] for course in courses))
    formatted_courses = [course.replace(" ", "") for course in courses]
    all_combinations = []

    for department in departments:
        module_counts = parseDepartmentData(term, department, formatted_courses)
        if module_counts:
            all_combinations.append(generateCourseCombos(module_counts))

    valid_times = []
    for combination in itertools.product(*all_combinations):
        days = sortByDays(combination)
        if overlapValidation(days):
            valid_times.append(combination)

    return valid_times