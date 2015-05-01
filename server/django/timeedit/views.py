import json

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
            print(course_post)
            try:
                course = Course.objects.get(course_code=course_post)
            except Course.DoesNotExist as e:
                try:
                    course = Course(**getCourseInfo(course_post))
                    course.save()
                except TypeError as e:
                    print(e)
                    return render(request, 'timeedit/index.html', {'form':form, 'message':'Sorry, cant handle your request! A codemonkey will be slayed for that!'})
                
            return render(request,
                          'timeedit/event.html',
                          {'course':course,
                           'events': getCourseEvents(course.season, course.year, course.course_anmalningskod)
                       }
            )
        return render(request, 'timeedit/index.html', {'form':form})



        
