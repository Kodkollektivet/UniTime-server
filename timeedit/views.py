# -*- coding:utf-8 -*-

import json
import logging

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import TemplateView

# Decorators
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Exceptions
from django.core.exceptions import *
from django.db import IntegrityError


from ipware.ip import get_ip

from .models import Course, Event, CourseCodes
from .forms import EventForm, CourseForm, CourseCodeForm
from .api.timeedit_handler import getCourseEvents, getCourseId, getCourseInfo


def createJsonCourse(listIn):

    return_data = []

    for course in listIn:
        data = {
            'name_sv': course.name_sv,
            'name_en': course.name_en,
            'course_code': course.course_code,
            'course_id': course.course_id,
            'course_points': course.course_points,
            'course_location': course.course_location,
            'course_language': course.course_language,
            'course_speed': course.course_speed,
            'syllabus_sv': course.syllabus_sv,
            'syllabus_en': course.syllabus_en,
            'semester': course.semester,
            'url': course.url,
            'year': course.year
        }
        return_data.append(data)

    return return_data


class IndexView(generic.View):

    '''
    This is the main Index view for the web gui
    '''

    # GET , return empty form
    def get(self, request, *args, **kwargs):
        
        # Create empty form
        form = CourseForm()

        # Return form
        return render(request, 'timeedit/index.html', {'form': form})

    # POST, 
    def post(self, request, *args, **kwargs):

        # Create new form and pass in post info.
        form = CourseForm(request.POST)
        
        searchLogger = logging.getLogger('searchLogger')
        defaultLogger = logging.getLogger('defaultLogger')
        errorLogger = logging.getLogger('errorLogger')
        ip = get_ip(request)

        # If form is valid
        if form.is_valid():

            # variable with cleaned data from the form
            course_post = form.cleaned_data['course'].upper()

            # Set seesion
            if 'course' in request.session.keys():
                if course_post not in request.session['course']:
                    request.session['course'].append(course_post)
            else:
                request.session['course'] = []

            # Logs a valid post before it reaches api_handler
            searchLogger.info('Search Term: %s  IP Addr: %s' % (course_post, ip))
            defaultLogger.info('Searching for %s...' % course_post)
            
            # Try to get if course from database
            try:
                defaultLogger.info('Looking for single course object in database...')
                
                # If there is only one course for the course code in database
                course = Course.objects.get(course_code=course_post)
                course_events = getCourseEvents(course.semester, course.year, course.course_reg)
                
                # Logs a fetch from the db
                defaultLogger = logging.getLogger('defaultLogger')
                defaultLogger.info('----------------FETCHED FROM DB---------------')
                defaultLogger.info('Course: %s' % course_post)
                defaultLogger.info('Single object')
                defaultLogger.info('-----------------END OF FETCH-----------------')
                defaultLogger.info(' ')
                
                return render(request,
                              'timeedit/index.html',
                              {'course' : course,
                               'events' : course_events,
                               'form' : form}
                )
             
            # If there is multiple course objects in the database
            except MultipleObjectsReturned as e:
                defaultLogger.info('Looking for multiple course object in database...')
                
                courses = Course.objects.filter(course_code = course_post)
                course_events_list = []
                 
                for i in courses:
                    course_events_list.append(getCourseEvents(i.semester, i.year, i.course_reg))
                    
                # Logs a fetch from the db
                defaultLogger.info('------------------FETCHED FROM DB-----------------')
                defaultLogger.info('Course: %s' % course_post)
                defaultLogger.info('Multiple Objects')
                defaultLogger.info('-------------------END OF FETCH-------------------')
                defaultLogger.info(' ')
                
                return render(request,
                              'timeedit/index.html',
                              {'course' : courses[0],
                               'events' : max(course_events_list),
                               'form' : form}
                )

            # If course dont exist in the database, request it
            except Course.DoesNotExist as e:
                defaultLogger.info('No matching course found in database. Requesting from TimeEdit...')
                 
                try:
                    
                    defaultLogger.info('----------------INITIATING REQUEST----------------')
                    
                    courses_list_id = getCourseId(course_post)  # The stupid id thats is assigned to every course
                    events_list = []
                    courses_list = []
                    
                    for i in courses_list_id:
                        course = Course(**getCourseInfo(i))
                        course.save()
                        courses_list.append(course)
                        
                    first_course = courses_list[0]
                        
                    for i in courses_list:
                        events_list.append(getCourseEvents(i.semester, i.year, i.course_reg))
                        
                    defaultLogger.info('------------------END OF REQUEST-----------------')
                        
                    return render(request,
                                  'timeedit/index.html',
                                  {'course' : first_course,
                                   'events' : max(events_list),
                                   'form' : form}
                              )
                except IndexError as e:
                    
                    defaultLogger.info('Request failed due to IndexError Exception in IndexView.post')
                    defaultLogger.info(e)
                    defaultLogger.info('------------------END OF REQUEST------------------')

                    errorLogger.info('Request failed due to IndexError Exception in IndexView.post')
                    errorLogger.info('Course: %s' % course_post)
                    errorLogger.info(e)
                    errorLogger.info('-')
                    
                    return render(request, 'timeedit/index.html', {'form':form, 'message':'Course does not exist, or is not active!'})

        # If form in not valid
        else:
            # Logs the post if it does not pass the form validation
            invalid_post = form.data['course']
            searchLogger.info('Invalid Search Term: %s  IP Addr: %s' % (invalid_post, ip))
            
            # Renders an error response
            return render(request, 'timeedit/index.html', {'form':form, 'message':'Invalid search format!'})


'''
API endpoint
'''
class CourseView(generic.View):

    '''
    This method is for accepting client requests that dont provide a csrf token.
    '''
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseView, self).dispatch(request, *args, **kwargs)
    
    '''    
    This GET returns ALL courses WITH info, can be much data here so be aware!
    '''
    def get(self, request, *args, **kwargs):
        
        # Returns json of all of the Courses that are saved in the database! Be aware of big data!

        courses = Course.objects.all()

        buffer_list = []
        for c in courses:
            if c not in buffer_list:
                buffer_list.append(c)
            else:
                pass

        course_list = []
        for course in buffer_list:
            data = {
                'course_code': course.course_code,
                'name_en': course.name_en,
                'name_sv': course.name_sv,
            }

            course_list.append(data)
        #list({{'course_code':c.course_code}: c for c in Course.objects.all()})
        #return HttpResponse(json.dumps(course_list), content_type='application/json')
        return HttpResponse(json.dumps(course_list), content_type='application/json')

    # This only returns the length of Course.objects.all()
    def head(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps({'satan':'satan'}), content_type='application/json')
        response['Content-Length'] = len(Course.objects.all())
        return response

    '''
    When POST here, only the specific course info will be sen
    '''
    def post(self, request, *args, **kwargs):

        # Create new form and pass in post info.
        form = CourseForm(request.POST)

        searchLogger = logging.getLogger('searchLogger')
        ip = get_ip(request)

        # If form is valid
        if form.is_valid():
            # variable with cleaned data from the form
            course_post = form.cleaned_data['course'].upper()
            
            # Logs a valid post before it reaches api_handler
            searchLogger.info('Search Term: %s  IP Addr: %s' % (course_post, ip))
            
            # Try to get if course from database
            try:
                # If there is only one course for the course code in database
                course = Course.objects.get(course_code=course_post)
                # Logs a fetch from the db
                defaultLogger = logging.getLogger('defaultLogger')
                defaultLogger.info('----------------FETCHED FROM DB---------------')
                defaultLogger.info('Course: %s' % course_post)
                defaultLogger.info('-----------------END OF FETCH-----------------')
                defaultLogger.info(' ')

                return HttpResponse(json.dumps(createJsonCourse([course])), content_type='application/json')

            # If there is mulit course objects in the database
            except MultipleObjectsReturned as e:
                courses = Course.objects.filter(course_code=course_post)
                return HttpResponse(json.dumps(createJsonCourse([courses[0]])), content_type='application/json')

            # If course dont exist in the database
            except Course.DoesNotExist as e:

                try:
                    courses_list_id = getCourseId(course_post)  # The stupid id thats is assigned to every course
                    courses_list = []
                
                    for i in courses_list_id:
                        course = Course(**getCourseInfo(i))
                        course.save()
                        courses_list.append(course)
                        
                    try:
                        return HttpResponse(json.dumps(createJsonCourse([courses_list[0]])), content_type='application/json')
                    
                    except ValueError as e:
                        print(e)
                        return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json', status=406)

                except IndexError as e:
                    print(e)
                    return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json', status=406)

        # If form in not valid
        else:
            # Logs the post if it does not pass the form validation
            invalid_post = form.data['course']
            searchLogger.info('Invalid Search Term: %s  IP Addr: %s' % (invalid_post, ip))
            
            # Renders an error response
            return HttpResponse(json.dumps({'message': 'Invalid search format!'}), content_type='application/json', status=406)


def course_by_code(request, course_code_in):


    # Create new form and pass in post info.
    form = CourseForm({'course':course_code_in})

    searchLogger = logging.getLogger('searchLogger')
    ip = get_ip(request)

    # If form is valid
    if form.is_valid():
        # variable with cleaned data from the form
        course_post = form.cleaned_data['course'].upper()

        # Logs a valid post before it reaches api_handler
        searchLogger.info('Search Term: %s  IP Addr: %s' % (course_post, ip))

        # Try to get if course from database
        try:
            # If there is only one course for the course code in database
            course = Course.objects.get(course_code=course_post)
            # Logs a fetch from the db
            defaultLogger = logging.getLogger('defaultLogger')
            defaultLogger.info('----------------FETCHED FROM DB---------------')
            defaultLogger.info('Course: %s' % course_post)
            defaultLogger.info('-----------------END OF FETCH-----------------')
            defaultLogger.info(' ')

            return HttpResponse(json.dumps(createJsonCourse([course])), content_type='application/json')

        # If there is mulit course objects in the database
        except MultipleObjectsReturned as e:
            courses = Course.objects.filter(course_code=course_post)
            return HttpResponse(json.dumps(createJsonCourse([courses[0]])), content_type='application/json')

        # If course dont exist in the database
        except Course.DoesNotExist as e:

            try:
                courses_list_id = getCourseId(course_post)  # The stupid id thats is assigned to every course
                courses_list = []

                for i in courses_list_id:
                    course = Course(**getCourseInfo(i))
                    course.save()
                    courses_list.append(course)

                try:
                    return HttpResponse(json.dumps(createJsonCourse([courses_list[0]])), content_type='application/json')

                except ValueError as e:
                    print(e)
                    return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json', status=406)

            except IndexError as e:
                print(e)
                return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json', status=406)

    # If form in not valid
    else:
        # Logs the post if it does not pass the form validation
        invalid_post = form.data['course']
        searchLogger.info('Invalid Search Term: %s  IP Addr: %s' % (invalid_post, ip))

        # Renders an error response
        return HttpResponse(json.dumps({'message': 'Invalid search format!'}), content_type='application/json', status=406)




'''
API endpoint
'''
class EventView(generic.View):
    
    """
    This method is for accepting client requests that dont provide a csrf token.
    """
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EventView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # Create new form and pass in post info.
        form = CourseForm(request.POST)
        #print(request.POST)
        
        searchLogger = logging.getLogger('searchLogger')
        ip = get_ip(request)

        # If form is valid
        if form.is_valid():

            # variable with cleaned data from the form
            course_post = form.cleaned_data['course'].upper()
            
            # Logs a valid post before it reaches api_handler
            searchLogger.info('Search Term: %s  IP Addr: %s' % (course_post, ip))
            
            # Try to get if course from database
            try:
                # If there is only one course for the course code in database
                course = Course.objects.get(course_code = course_post)
                # Logs a fetch from the db
                defaultLogger = logging.getLogger('defaultLogger')
                defaultLogger.info('----------------FETCHED FROM DB---------------')
                defaultLogger.info('Course: %s' % course_post)
                defaultLogger.info('-----------------END OF FETCH-----------------')
                defaultLogger.info(' ')
                return HttpResponse(json.dumps(getCourseEvents(course.semester,
                                                               course.year,
                                                               course.course_reg,
                                                               course_post,
                                                               course.name_en,
                                                               course.name_sv)), content_type='application/json')

            # If there is mulit course objects in the database
            except MultipleObjectsReturned as e:
                courses = Course.objects.filter(course_code = course_post)
                course_events_list = []
                
                for i in courses:
                    course_events_list.append(getCourseEvents(i.semester,
                                                              i.year,
                                                              i.course_reg,
                                                              course_post,
                                                              i.name_en,
                                                              i.name_sv))

                return HttpResponse(json.dumps(max(course_events_list)), content_type='application/json')

            # If course dont exist in the database
            except Course.DoesNotExist as e:

                try:
                    courses_list_id = getCourseId(course_post)  # The stupid id thats is assigned to every course
                    events_list = []
                    courses_list = []
                
                    for i in courses_list_id:
                        course = Course(**getCourseInfo(i))
                        course.save()
                        courses_list.append(course)

                    for i in courses_list:
                        events_list.append(getCourseEvents(i.semester,
                                                           i.year,
                                                           i.course_reg,
                                                           course_post,
                                                           i.name_en,
                                                           i.name_sv))
                    
                    try:
                        return HttpResponse(json.dumps(max(events_list)), content_type='application/json')
                    
                    except ValueError as e:
                        print(e)
                        return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json')

                except IndexError as e:
                    print(e)
                    return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json')

        # If form in not valid
        else:
            # Logs the post if it does not pass the form validation
            invalid_post = form.data['course']
            searchLogger.info('Invalid Search Term: %s  IP Addr: %s' % (invalid_post, ip))
            
            # Renders an error response
            return HttpResponse({'message':'Invalid search format!'})


def events_by_code(request, course_code_in):
    # Create new form and pass in post info.
    form = CourseForm({'course':course_code_in})
    #print(request.POST)

    searchLogger = logging.getLogger('searchLogger')
    ip = get_ip(request)

    # If form is valid
    if form.is_valid():

        # variable with cleaned data from the form
        course_post = form.cleaned_data['course'].upper()

        # Logs a valid post before it reaches api_handler
        searchLogger.info('Search Term: %s  IP Addr: %s' % (course_post, ip))

        # Try to get if course from database
        try:
            # If there is only one course for the course code in database
            course = Course.objects.get(course_code = course_post)
            # Logs a fetch from the db
            defaultLogger = logging.getLogger('defaultLogger')
            defaultLogger.info('----------------FETCHED FROM DB---------------')
            defaultLogger.info('Course: %s' % course_post)
            defaultLogger.info('-----------------END OF FETCH-----------------')
            defaultLogger.info(' ')
            return HttpResponse(json.dumps(getCourseEvents(course.semester,
                                                           course.year,
                                                           course.course_reg,
                                                           course_post,
                                                           course.name_en,
                                                           course.name_sv)), content_type='application/json')

        # If there is mulit course objects in the database
        except MultipleObjectsReturned as e:
            courses = Course.objects.filter(course_code = course_post)
            course_events_list = []

            for i in courses:
                course_events_list.append(getCourseEvents(i.semester,
                                                          i.year,
                                                          i.course_reg,
                                                          course_post,
                                                          i.name_en,
                                                          i.name_sv))

            return HttpResponse(json.dumps(max(course_events_list)), content_type='application/json')

        # If course dont exist in the database
        except Course.DoesNotExist as e:

            try:
                courses_list_id = getCourseId(course_post)  # The stupid id thats is assigned to every course
                events_list = []
                courses_list = []

                for i in courses_list_id:
                    course = Course(**getCourseInfo(i))
                    course.save()
                    courses_list.append(course)

                for i in courses_list:
                    events_list.append(getCourseEvents(i.semester,
                                                       i.year,
                                                       i.course_reg,
                                                       course_post,
                                                       i.name_en,
                                                       i.name_sv))

                try:
                    return HttpResponse(json.dumps(max(events_list)), content_type='application/json')

                except ValueError as e:
                    print(e)
                    return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json')

            except IndexError as e:
                print(e)
                return HttpResponse(json.dumps({'message': 'Can not find that course'}), content_type='application/json')

    # If form in not valid
    else:
        # Logs the post if it does not pass the form validation
        invalid_post = form.data['course']
        searchLogger.info('Invalid Search Term: %s  IP Addr: %s' % (invalid_post, ip))

        # Renders an error response
        return HttpResponse({'message':'Invalid search format!'})



'''
Endpoint for web gui autocomplete
'''
def allCouseCodesInJSON(request):
    #return HttpResponse(json.dumps(list({c.course_code: c for c in Course.objects.all()})),content_type='application/json')
    return HttpResponse(json.dumps(list(request.session['course'])),content_type='application/json')

'''
API endpoint
'''
def allCoursesInJSON(request):
    return HttpResponse(json.dumps(serializers.serialize('json', Course.objects.all())), content_type='application/json')



class AddCourseCodeView(generic.View):

    '''
    This endpoints is only for collecting course codes
    '''
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddCourseCodeView, self).dispatch(request, *args, **kwargs)

    '''
    When POST here, only the specific course info will be sen
    '''
    def post(self, request, *args, **kwargs):

        # Create new form and pass in post info.
        form = CourseCodeForm(request.POST)

        # If form is valid
        if form.is_valid():
            # variable with cleaned data from the form
            course_code = form.cleaned_data['code'].upper()

            try:
                code = CourseCodes(code=course_code)
                code.save()
                return HttpResponse(json.dumps({'status':'ok'}), content_type='application/json')

            except KeyError as e:
                print(e)
                return HttpResponse(json.dumps({'status': 'wrong'}), content_type='application/json')


            except IntegrityError as e:
                print(e)
                return HttpResponse(json.dumps({'status': 'already added'}), content_type='application/json')

        else:
            return HttpResponse(json.dumps({'status': 'form errors'}), content_type='application/json')

    '''
    This GET returns ALL course codes!
    '''
    def get(self, request, *args, **kwargs):
        # Returns all of the course codes.
        return HttpResponse(json.dumps([{'code':c.code} for c in CourseCodes.objects.all()]), content_type='application/json')