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

from .models import Course, Event
from .forms import EventForm, CourseForm
from .api_handler import getCourseInfo, getCourseEvents

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        form = CourseForm()
        return render(request, 'timeedit/index.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            course_post = form.cleaned_data['course'].upper()
            
            # Log
            searchLogger = logging.getLogger('searchLogger')
            searchLogger.info(course_post) # Logs the search post before it reaches the api_handler
            
            #print(course_post) #Not working with öäå
            try:
                course = Course.objects.get(course_code=course_post)
                
                defaultLogger = logging.getLogger('defaultLogger')                
                defaultLogger.info('----------------FETCHED FROM DB---------------')
                defaultLogger.info('Course: %s' % course_post)
                defaultLogger.info('-----------------END OF FETCH-----------------')
                defaultLogger.info(' ')
                
            except Course.DoesNotExist as e:
                try:
                    course = Course(**getCourseInfo(course_post))
                    course.save()
                except TypeError as e:
                    print(e)
                    return render(request, 'timeedit/index.html', {'form':form, 'message':'Sorry, we cant handle your request! We are working on fixing this!'})
                
            return render(request,
                          'timeedit/index.html',
                          {'course' : course,
                           'events' : getCourseEvents(course.season, course.year, course.course_anmalningskod),
                           'form' : form,
                       }
            )
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

    def post(self, request, *args, **kwargs):
        pass

def allCouseCodesInJSON(request):
    return HttpResponse(json.dumps(map(lambda c: c.course_code, Course.objects.all())),content_type='application/json')

        
def allCoursesInJSON(request):
    return HttpResponse(json.dumps(serializers.serialize('json', Course.objects.all())), content_type='application/json')


