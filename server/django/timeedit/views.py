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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseView, self).dispatch(request, *args, **kwargs)
        
    # This GET returns ALL courses WITH info, can be much data here so be aware!
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(serializers.serialize('json', Course.objects.all())), content_type='application/json')

    # When POST here, only the specific course info will be sent
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        print(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course'].upper()
            try:
                return HttpResponse(json.dumps(serializers.serialize('json', [Course.objects.get(course_code=course),])), content_type='application/json')
            except Course.DoesNotExist as e:
                return HttpResponse(json.dumps({'message':'Can not find that course'}), content_type='application/json')
        return HttpResponse(json.dumps({'message':'Invalid input'}), content_type='application/json')
        
class EventView(generic.View):

    def post(self, request, *args, **kwargs):
        pass

def allCouseCodesInJSON(request):
    return HttpResponse(json.dumps(map(lambda c: c.course_code, Course.objects.all())),content_type='application/json')

        
def allCoursesInJSON(request):
    return HttpResponse(json.dumps(serializers.serialize('json', Course.objects.all())), content_type='application/json')


