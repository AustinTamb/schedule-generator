#!/usr/bin/env python
import re

def clean_string(raw_string):
    raw_string = raw_string.replace("</strong>", "").replace("<br>", "").replace("\n", " ").replace("\t", "")
    return raw_string.replace("</td>", "").replace("</tr>", "")


with open("sequence.html", "r") as f:
    contents = f.read().replace("&nbsp", "").replace("<em>", "").replace("</em>", "")
    s_i, e_i = contents.find("<table>"), contents.find("</table>")
    contents = contents[s_i:e_i]
    tr_split = contents.split("<tr>")[2:-1]
    courses = {}
    or_courses = {}
    for i in tr_split:
        td_split = i.split("<td>")[2:]
        
        for j in td_split:
            strong_split = j.split("<strong>")
            next_is_or = False

            for k in strong_split:
                if k == '':
                    continue
                index = k.find("|")
                course_code = clean_string(k[:index-1])
                if "Elective" in course_code:
                    course_name = "-"
                else:
                    course_name = clean_string(k[index+2:])

                if "</td>" in course_name:
                    td_index = course_name.find("</td>")
                    course_name = course_name[:td_index]

                if "OR" == course_name[-2:]:
                    or_courses[course_code] = course_name[:-2]
                    next_is_or = True
                elif next_is_or:
                    or_courses[course_code] = course_name
                    next_is_or = False
                else:
                    courses[course_code] = course_name

    ite = 0
    for key, value in courses.items():
        print("{0} {1}".format(key, value))
        ite += 1
        
    for key, value in or_courses.items():
        print(key, value)
        ite += 1
    print(ite)
    
