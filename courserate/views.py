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

from .models import Rate

'''
API endpoint for rating course
'''
class CourseRateView(generic.View):

    '''
    This method is for accepting client requests that dont provide a csrf token.
    '''
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseRateView, self).dispatch(request, *args, **kwargs)

    '''
    This GET returns ALL courses WITH info, can be much data here so be aware!
    '''
    def post(self, request, *args, **kwargs):
        print(request.POST)
        try:
            rate = Rate(
                course_code= request.POST['course_code'],
                course_rate= int(request.POST['course_rate']),
                notes = request.POST['notes'],
                ip = get_ip(request),
                )
            rate.save()
            return HttpResponse(json.dumps({'message': 'okey'}), content_type='application/json')
        except IOError as e:
            print(e)

        except IntegrityError as e:
            print(e)
            return HttpResponse(json.dumps({'message': 'Cant rate a course more than 1 time.'}), content_type='application/json')



