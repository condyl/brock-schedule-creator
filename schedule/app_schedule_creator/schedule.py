import itertools
import selenium
from.models import Course

def get_course_options(courses,term,year):
    times = []

    for course in courses:
        course_options = Course.objects.filter(course_code=course, course_term=term, course_year=year)
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

    # get all possible combinations of course options for all courses
    valid_times = []
    all_times = list(itertools.product(*times)) 
    for time in all_times:
        days = {
            "M": [],
            "T": [],
            "W": [],
            "R": [],
            "F": []
        }
        for course in time:
            # organise course options by day
            for course_option in course:
                if "M" in course_option.course_days: days["M"].append([str(course_option.course_start_time), str(course_option.course_end_time), str(course_option.course_start_date), str(course_option.course_end_date)])
                if "T" in course_option.course_days: days["T"].append([str(course_option.course_start_time), str(course_option.course_end_time), str(course_option.course_start_date), str(course_option.course_end_date)])
                if "W" in course_option.course_days: days["W"].append([str(course_option.course_start_time), str(course_option.course_end_time), str(course_option.course_start_date), str(course_option.course_end_date)])
                if "R" in course_option.course_days: days["R"].append([str(course_option.course_start_time), str(course_option.course_end_time), str(course_option.course_start_date), str(course_option.course_end_date)])
                if "F" in course_option.course_days: days["F"].append([str(course_option.course_start_time), str(course_option.course_end_time), str(course_option.course_start_date), str(course_option.course_end_date)])

        valid = True
        for day in days:
            # sort class times by start time
            days[day] = sorted(days[day])
            for i in range(len(days[day]) - 1):
                # eliminate overlapping class times from the valid courses
                # if ((overlapping or start times are the same) and not (end time of first class is before start time of second class)
                #if ((days[day][i][1] > days[day][i + 1][0]) or days[day][i][0] == days[day][i + 1][0]) and not (days[day][i][2] < days[day][i + 1][3]):
                #    valid = False
                #    break


                # 0: start time
                # 1: end time
                # 2: start date
                # 3: end date

                # if classes start/end at the same time, and start/end at the same dates, they are invalid
                if (days[day][i][0] == days[day][i+1][0] or days[day][i][1] == days[day][i+1][1]) and (days[day][i][2] == days[day][i+1][2] or days[day][i][3] == days[day][i+1][3]):
                    valid = False
                    break
                ## if classes are within 
                #elif days[day][i][0] < days[day][i+1][0] and days[day][i][1] > days[day][i+1][0]:
                #    valid = False
                #    break

            
        if valid:
            valid_times.append(time)

    return valid_times






    

