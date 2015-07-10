# -*- coding:utf-8 -*-

'''
This method cant find all courses!
Use only as backup if other functions dont work
'''

import httplib
import json
import requests
import re
import pprint
import datetime
import logging

from django.http import HttpResponse

from ..models import Course

defaultLogger = logging.getLogger('defaultLogger')
errorLogger = logging.getLogger('errorLogger')

__THIS_YEAR = datetime.datetime.now().strftime('%y')
__THIS_SEMESTER = ''
__MONTH_NOW = int(datetime.datetime.now().strftime('%m'))


# Evaluate if now() is HT or VT
if (__MONTH_NOW <= 6):
    __THIS_SEMESTER = 'VT'
else:
    __THIS_SEMESTER = 'HT'

    
# Simple page scrapper
# looking for Anmälningskod and if its Vår och Höst (HT / VT)
def getCourseInfo_scrapper(course):
    # send the request with couser ex 1DV008
    #'http://lnu.se/utbildning/kurser/%s#semseter_20%s1' % (course, __THIS_YEAR) 
    url = 'http://lnu.se/utbildning/kurser/%s' % (course) 
    req = requests.get(url)
 
    # see if anmälningskod is in the page
    match_code_regexp = re.compile(r'LNU-\d\d\d\d\d', re.M|re.I)  # the regexp
    match_codes = match_code_regexp.findall(req.text)             # find all of the matches, we may find many
    match_codes = map(lambda x:x.strip('LNU-'), match_codes)  # remove LNU- from matches
    if match_codes:
        defaultLogger.info('-------------SUCCSESSFUL REQUEST--------------')
        defaultLogger.info('Course: %s' % course)
        defaultLogger.info('URL: %s' % url)
        defaultLogger.info('Request response: %s' % req)
        defaultLogger.info('----------------END OF REQUEST----------------')
        defaultLogger.info(' ')
        return {
            'course_code':course,
            'course_anmalningskod':match_codes[0],  # take only the first in the list
            'season': __THIS_SEMESTER,
            'html_url':url,
            'year':__THIS_YEAR,
        }

    else:

        defaultLogger.info('----------------FAILED REQUEST---------------')
        defaultLogger.info('Course: %s' % course)
        defaultLogger.info('URL: %s' % url)
        defaultLogger.info('Request response: %s' % req)
        defaultLogger.info('----------------END OF REQUEST---------------')
        defaultLogger.info(' ')
        
        errorLogger.info('MISMATCHED CODE: %s' % course)
        errorLogger.info('URL: %s' % url)
        errorLogger.info('-------------------------------------------')
        
        print('Course not found') # Course cant print, problem with utf encoding

def getAllCourseCodes_scrapper(request):

    url = 'http://lnu.se/utbildning/kurser'
    req = requests.get(url)                                # the request
    # see if anmälningskod is in the page
    match_code = re.compile(r'\(\d...\d\d\)', re.M|re.I)   # the regexp
    all_courses = match_code.findall(req.text)             # find all of the course_anmalningskod
    all_courses = map(lambda x:x.strip('()'), all_courses) # strip away all of the ()
    for i in all_courses:
        try:
            new_course = Course(**getCourseInfo(i))
            new_course.save()
        except TypeError:
            print('couldnt save: '+i)
        print(new_course.course_code + ' saved......')
    return HttpResponse('Everything stored....')

#This work like public static void main in Java
# if __name__ == '__main__':
#     course = getCourseInfo('1BD101')
#     print(getCourseEvents(course['season'], course['year'], course['course_anmalningskod']))
#     all_courses = getAllCourseCodes()
#     for i in range(0, 50):
#         print(getCourseInfo(all_courses[i]))
        
