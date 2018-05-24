import re
import urllib.request

def clean_string(raw_string):
    raw_string = raw_string.replace("</strong>", "").replace("<br>", "").replace("\n", " ").replace("\t", "")
    return raw_string.replace("</td>", "").replace("</tr>", "").replace("<br />", "").replace("<br", "")

def get_course_dicts(program="", year=""):
    """
    Given a program name and course sequence year, this attempts to get the courses
    from the website. 

    :program: Program of study
    :year: Course sequence year
    
    :return: dict - Contains courses
             dict - Contains x or y courses
    """
    programs = {"Software Engineering":"software", "Electrical Engineering":"electrical"}
    
    program = programs.get(program, program)
    url = "http://engineering.uottawa.ca/about/programs/undergraduate/{0}-{1}".format(program, year)
    f = urllib.request.urlopen(url)
    
    contents = f.read().decode("utf-8").replace("&nbsp", "").replace("<em>", "").replace("</em>", "")
    s_i, e_i = contents.find("<table>"), contents.find("</table>")
    contents = contents[s_i:e_i]
    tr_split = contents.split("<tr>")[2:-1]
    courses = {}
    or_courses = [[]]
    for i in tr_split:
        td_split = i.split("<td>")[2:]
            
        for j in td_split:
            strong_split = j.split("<strong>")
            next_is_or = False
            or_index = 0
            for k in strong_split:
                if k == '':
                    continue
                index = k.find("|")
                course_code = clean_string(k[:index-1])
                if "Elective" in course_code:
                    course_name = "-"
                else:
                    course_name = clean_string(k[index+1:])

                if "</td>" in course_name:
                    td_index = course_name.find("</td>")
                    course_name = course_name[:td_index]

                if "OR" == course_name[-2:]:
                    courses[course_code] = course_name[:-2]
                    or_courses[or_index].append(course_code)
                    next_is_or = True
                elif next_is_or:
                    courses[course_code] = course_name
                    or_courses[or_index].append(course_code)
                    #or_courses.append([])
                    or_index += 1
                    next_is_or = False
                else:
                    courses[course_code] = course_name

    return courses, or_courses
    
courses, ors = get_course_dicts("Electrical Engineering", "2017")

for i in courses:
    print(i, courses[i])

for i, group in enumerate(ors):
    print("Or Group {0}:".format(i+1))
    for j in group:
        print(j, courses[j])