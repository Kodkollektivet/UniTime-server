# -*- coding:utf-8 -*-

import json
import logging

from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Course, Event
from .forms import EventForm
from .api_handler import getCourseInfo, getCourseEvents

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, 'timeedit/index.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
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
                    return render(request, 'timeedit/index.html', {'form':form, 'message':'Sorry, cant handle your request! A codemonkey will be slayed for that!'})
                
            return render(request,
                          'timeedit/index.html',
                          {'course' : course,
                           'events' : getCourseEvents(course.season, course.year, course.course_anmalningskod),
                           'form' : form,
                       }
            )
        return render(request, 'timeedit/index.html', {'form':form})



        
