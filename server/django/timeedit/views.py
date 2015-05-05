# -*- coding:utf-8 -*-

import json
import logging

from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import serializers

# Decorators
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ipware.ip import get_ip

from .models import Course, Event
from .forms import EventForm, CourseForm
from .api.timeedit_handler import getCourseEvents, getCourseId, getCourseInfo
from .scrapper.lnu_course_page_scrapper import getCourseInfo_scrapper, getAllCourseCodes_scrapper


class IndexView(generic.View):

    '''
    This is the main Index view for the web gui
    '''

    # GET , return empty form
    def get(self, request, *args, **kwargs):
        
        # Create empty form
        form = CourseForm()

        # Return empty form with request, template, form
        return render(request, 'timeedit/index.html', {'form':form})

    # POST, 
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
            
            #print(course_post) #Not working with öäå

            # Try to get if course from database
            try:
                
                course = Course.objects.filter(course_code=course_post)
                
                # Logs a fetch from the db
                defaultLogger = logging.getLogger('defaultLogger')
                defaultLogger.info('----------------FETCHED FROM DB---------------')
                defaultLogger.info('Course: %s' % course_post)
                defaultLogger.info('-----------------END OF FETCH-----------------')
                defaultLogger.info(' ')

            # If course dont exist in the database
            except Course.DoesNotExist as e:
                
                try:
                    course_id_list = getCourseId(course_post)
                    print(course_id_list)
                    for i in course_id_list:
                        try:
                            course = Course(**getCourseInfo(i))
                            course.save()
                        except IOError as e:
                            print(e)

                except TypeError as e:
                    print(e)
                    return render(request, 'timeedit/index.html', {'form':form, 'message':'Sorry, we cant handle your request! We are working on fixing this!'})


                except IndexError as e:
                    print(e)
                    return render(request, 'timeedit/index.html', {'form':form, 'message':'The requested course could not be found!'})

            list_with_courses_events = []
            print('here')
            for i in Course.objects.filter(course_code=course_post):
                events = getCourseEvents(i.semester, i.year, i.course_reg)
                list_with_courses_events.append(events)
                print(events)

            return render(request,
                          'timeedit/index.html',
                          {'course' : course[0],
                           'events' : max(list_with_courses_events),
                           'form' : form,
                       }
            )
        else:
            print('Not valid')
            # Logs the post if it does not pass the form validation
            invalid_post = form.data['course']
            searchLogger.info('Invalid Search Term: %s  IP Addr: %s' % (invalid_post, ip))
            
            # Renders an error response
            return render(request, 'timeedit/index.html', {'form':form, 'message':'Invalid search format!'})
        return render(request, 'timeedit/index.html', {'form':form})

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
        return HttpResponse(json.dumps(serializers.serialize('json', Course.objects.all())), content_type='application/json')

    
    '''
    When POST here, only the specific course info will be sen
    '''
    def post(self, request, *args, **kwargs):

        # Empty form, the reason a form i here is because we do data validation with forms. Check out CourseForm inside of forms.py
        form = CourseForm(request.POST)
        print(request.POST)
        # If form data is valid, continue. Else send error messages
        if form.is_valid():

            # Get the cleaned data from the form.
            course = form.cleaned_data['course'].upper()

            # Try to get the object from the database
            try:

                # If object is found, serialize it and send it as json
                return HttpResponse(json.dumps(serializers.serialize('json', [Course.objects.get(course_code=course),])), content_type='application/json')

            # If object not found in database, send this
            except Course.DoesNotExist as e:

                # Send a simple json object with error message
                return HttpResponse(json.dumps({'message':'Can not find that course'}), content_type='application/json')

        # If form is invalid, send simple json object
        return HttpResponse(json.dumps({'message':'Invalid input'}), content_type='application/json')

    
class EventView(generic.View):
    
    '''
    This method is for accepting client requests that dont provide a csrf token.
    '''
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EventView, self).dispatch(request, *args, **kwargs)

    
    def post(self, request, *args, **kwargs):
        pass
        # Empty form, the reason a form i here is because we do data validation with forms. Check out CourseForm inside of forms.py
        form = CourseForm(request.POST)

        # If form data is valid, continue. Else send error messages
        if form.is_valid():

            # Get the cleaned data from the form.
            course = form.cleaned_data['course'].upper()

            # Try to get the object from the database
            try:
                # Course object from database
                course_object = Course.objects.get(course_code=course)
                
                # If object is found, serialize it to the getCourseEvents function
                # This function calls LNUs timeedit API, this API returns JSON
                return HttpResponse(json.dumps(getCourseEvents(course_object.season, course_object.year, course_object.course_anmalningskod)), content_type='application/json')

            # If object not found in database, send this
            except Course.DoesNotExist as e:

                # Send a simple json object with error message
                return HttpResponse(json.dumps({'message':'Can not find that course'}), content_type='application/json')

        # If form is invalid, send simple json object
        return HttpResponse(json.dumps({'message':'Invalid input'}), content_type='application/json')

    
def allCouseCodesInJSON(request):
    return HttpResponse(json.dumps(map(lambda c: c.course_code, Course.objects.all())),content_type='application/json')

        
def allCoursesInJSON(request):
    return HttpResponse(json.dumps(serializers.serialize('json', Course.objects.all())), content_type='application/json')


