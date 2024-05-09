import itertools
import selenium
from.models import Course

def get_course_options(courses,term,year):
    times = []

    for course in courses:
        course_options = Course.objects.filter(course_code=course, course_term=term, course_year=year)
        #print(course_options[0])
        modules = []
        module_counts = {}
        # get all modules needed for course & how many options there are
        for course_option in course_options:
            if course_option.course_type[:3] not in modules:
                modules.append(course_option.course_type[:3])

            # separate course options by module
            try: # if we can append to the list --> it exists
                module_counts[course_option.course_type[:3]].append(course_option)
            except: # if we can't append to the list --> it doesn't exist --> create it
                module_counts[course_option.course_type[:3]] = [course_option]

        # get all possible combinations of course options
        options = list(itertools.product(*module_counts.values())) 
        
        times.append(options)

    #print("\nTIMES: ")
    # get all possible combinations of course options for all courses
    valid_times = []
    all_times = list(itertools.product(*times)) 
    for time in all_times:
        #print(time)
        days = {
            "M": [],
            "T": [],
            "W": [],
            "R": [],
            "F": []
        }
        for course in time:
            for course_option in course:
                #print(course_option[4])
                if "M" in course_option.course_days: days["M"].append([str(course_option.course_start_time), str(course_option.course_end_time)])
                if "T" in course_option.course_days: days["T"].append([str(course_option.course_start_time), str(course_option.course_end_time)])
                if "W" in course_option.course_days: days["W"].append([str(course_option.course_start_time), str(course_option.course_end_time)])
                if "R" in course_option.course_days: days["R"].append([str(course_option.course_start_time), str(course_option.course_end_time)])
                if "F" in course_option.course_days: days["F"].append([str(course_option.course_start_time), str(course_option.course_end_time)])

        valid = True
        for day in days:
            days[day] = sorted(days[day])
            for i in range(len(days[day]) - 1):
                if days[day][i][1] > days[day][i + 1][0]:
                    valid = False
            
        if valid:
            valid_times.append(time)
        #print(days)


    for v in valid_times:
        #print("\n")
        for course in v:
            for module in course:
                #print(module)
                pass

    return valid_times






    

