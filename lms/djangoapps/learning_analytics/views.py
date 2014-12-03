from edxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django_future.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.http import HttpResponse
import logging

from json import dumps

from analytics import (get_DB_sort_course_homework, 
                       get_DB_course_spent_time, 
                       get_DB_student_grades, 
                       get_DB_course_section_accesses)
from analytics_jose import get_DB_time_schedule
from data import get_course_key, get_course_module, get_course_students, get_course_grade_cutoff

from courseware.access import has_access
from courseware.masquerade import setup_masquerade
from courseware.models import StudentModule
from courseware.courses import get_course_with_access, get_studio_url
from courseware.views import fetch_reverify_banner_info


VISUALIZATIONS_ID = {'LA_course_sort_students': 0,
                     'LA_student_grades': 1,
                     'LA_chapter_time': 2,
                     'LA_course_accesses': 3,
                     'LA_time_schedule': 4,}

# Constants for student_id
ALL_STUDENTS = -1
PROF_GROUP = -2
PASS_GROUP = -3
FAIL_GROUP = -4

# Create your views here.

@login_required
@ensure_csrf_cookie
def index(request, course_id):
   
    # Request data
    course_key = get_course_key(course_id)
    course = get_course_module(course_key)
    user = request.user
    staff_access = has_access(request.user, 'staff', course)
    instructor_access = has_access(request.user, 'instructor', course)
    masq = setup_masquerade(request, staff_access)  # allow staff to toggle masquerade on info page
    studio_url = get_studio_url(course, 'course_info')
    reverifications = fetch_reverify_banner_info(request, course_key)
    
    # Proficiency and pass limit
    pass_limit = get_course_grade_cutoff(course)
    proficiency_limit = (1 - pass_limit) / 2 + pass_limit
    
    # Analytics visualizations
    if staff_access or instructor_access:
        # Instructor access
        # Sort homework
        std_sort = get_DB_sort_course_homework(course_key)
        # Chapter time
        cs, st = get_DB_course_spent_time(course_key, student_id=ALL_STUDENTS)
        students_spent_time = chapter_time_to_js(cs, st)
        students_grades = get_DB_student_grades(course_key, student_id=ALL_STUDENTS)
        cs, sa = course_accesses = get_DB_course_section_accesses(course_key, student_id=ALL_STUDENTS)
        students_course_accesses = course_accesses_to_js(cs, sa)
        students_time_schedule = get_DB_time_schedule(course_key, student_id=ALL_STUDENTS)
            
        
        context = {'course': course,
                   'request': request,
                   'user': user,
                   'staff_access': staff_access,
                   'instructor_access': instructor_access,
                   'masquerade': masq,
                   'studio_url': studio_url,
                   'reverifications': reverifications,
                   'course_id': course_id,
                   'students': students_to_js(get_course_students(course_key)),
                   'visualizations_id': VISUALIZATIONS_ID,
                   'std_grades_dump': dumps(students_grades),
                   'sort_std_dump': dumps(std_sort),
                   'time_dump': dumps(students_spent_time),
                   'accesses_dump': dumps(students_course_accesses),
                   'std_time_schedule_dumb': dumps(students_time_schedule),
                   'pass_limit': pass_limit,
                   'prof_limit': proficiency_limit,}
    else:
        # Student access
        
        # Chapter time
        cs, st = get_DB_course_spent_time(course_key, user.id)
        student_spent_time = chapter_time_to_js(cs, st)
        students_grades = get_DB_student_grades(course_key, user.id)
        cs, sa = course_accesses = get_DB_course_section_accesses(course_key, user.id)
        student_course_accesses = course_accesses_to_js(cs, sa)
        student_time_schedule = get_DB_time_schedule(course_key, user.id)
        
        
        context = {'course': course,
                   'request': request,
                   'user': user,
                   'staff_access': staff_access,
                   'instructor_access': instructor_access,
                   'masquerade': masq,
                   'studio_url': studio_url,
                   'reverifications': reverifications,
                   'course_id': course_id,
                   'students': students_to_js([user]),
                   'std_grades_dump': dumps(students_grades),
                   'sort_std_dump': None,
                   'time_dump': dumps(student_spent_time),
                   'accesses_dump': dumps(student_course_accesses),
                   'std_time_schedule_dumb': dumps(student_time_schedule),
                   'pass_limit': pass_limit,
                   'prof_limit': proficiency_limit,}
        
    return render_to_response('learning_analytics/learning_analytics.html', context)    


@login_required
@ensure_csrf_cookie
def chart_update(request):
    results = {'success' : False}
    chart_info_json = dumps(results)
    if request.method == u'GET':
        GET = request.GET
        course_key = get_course_key(GET[u'course_id'])
        user_id = GET[u'user_id']
        chart = int(GET[u'chart'])
        if chart == VISUALIZATIONS_ID['LA_chapter_time']:
            cs, st = get_DB_course_spent_time(course_key, student_id=user_id)
            student_spent_time = chapter_time_to_js(cs, st)
            chart_info_json = dumps(student_spent_time)
        elif chart == VISUALIZATIONS_ID['LA_course_accesses']:
            cs, sa = get_DB_course_section_accesses(course_key, student_id=user_id)
            student_course_accesses = course_accesses_to_js(cs, sa)
            chart_info_json = dumps(student_course_accesses)
        elif chart == VISUALIZATIONS_ID['LA_student_grades']:
            students_grades = get_DB_student_grades(course_key, student_id=user_id)
            chart_info_json = dumps(students_grades)
        elif chart == VISUALIZATIONS_ID['LA_time_schedule']:
            student_time_schedule = get_DB_time_schedule(course_key, student_id=user_id)
            chart_info_json = dumps(student_time_schedule)
    
    return HttpResponse(chart_info_json, mimetype='application/json')

def chapter_time_to_js(course_struct, students_time):
    """
    Formats time chapters data to send it to a javascript script
    """
    result = {}
    for st_id in students_time.keys():
        result[st_id] = []
        for chapter in course_struct:
            chapt_data = {'name': chapter['name'],
                          'total_time': students_time[st_id][chapter['id']]['time_spent']}
            graded_time = 0
            ungraded_time = 0
            for sequential in chapter['sequentials']:
                if sequential['graded']:
                    graded_time = (graded_time + 
                                   students_time[st_id][chapter['id']]['sequentials'][sequential['id']]['time_spent'])
                else:
                    ungraded_time = (ungraded_time + 
                                     students_time[st_id][chapter['id']]['sequentials'][sequential['id']]['time_spent'])
            
            chapt_data['graded_time'] = graded_time
            chapt_data['ungraded_time'] = ungraded_time
            result[st_id].append(chapt_data)
            
    return result


def students_to_js(students_user):
    result = []
    for user in students_user:
        result.append({'id':user.id, 'name':user.username })
    return result


def course_accesses_to_js(course_struct, students_course_accesses):
    """
    Formats course accesses data to send it to a javascript script
    """
    result = {}
    for st_id in students_course_accesses.keys():
        result[st_id] = []
        for chapter in course_struct:
            chapt_data = {'name': chapter['name'],
                          'accesses': students_course_accesses[st_id][chapter['id']]['accesses'],
                          'sequentials':[]}
            for sequential in chapter['sequentials']:
                seq_data = {'name': sequential['name'],
                            'accesses': students_course_accesses[st_id][chapter['id']]['sequentials'][sequential['id']]['accesses'],
                            'verticals':[]}
                for vertical in sequential['verticals']:
                    vert_data = {'name': vertical['name'],
                                 'accesses': students_course_accesses[st_id][chapter['id']]['sequentials'][sequential['id']]['verticals'][vertical['id']]['accesses']}
                    seq_data['verticals'].append(vert_data)
                chapt_data['sequentials'].append(seq_data)
            result[st_id].append(chapt_data)
    return result