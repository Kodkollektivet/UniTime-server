# -*- coding:utf-8 -*-

import json


from django.views import generic
from django.http import HttpResponse

# Decorators
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Exceptions
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

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
            return HttpResponse(json.dumps({'message': 'success'}), content_type='application/json', status=201)

        except MultiValueDictKeyError as e:
            print(e)
            return HttpResponse(json.dumps({'message': 'form errors'}), content_type='application/json', status=404)

        except IntegrityError as e:
            print(e)
            return HttpResponse(json.dumps({'message': 'Cant rate a course more than 1 time.'}), content_type='application/json', status=403)

        return HttpResponse(json.dumps({'message': 'Something is wrong'}), content_type='application/json', status=400)




