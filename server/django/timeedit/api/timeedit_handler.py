# -*- coding:utf-8 -*-

# Links that does not work
# http://lnu.se/utbildning/kurser/1MA164

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
__WEEK_NOW = datetime.datetime.now().isocalendar()[1] # Not used

# Evaluate if now() is HT or VT
if (__MONTH_NOW <= 6):
    __THIS_SEMESTER = 'VT'
else:
    __THIS_SEMESTER = 'HT'

    
# course here is Anmälningskod
# season is VT or HT
# year is __THISYEAR
def getCourseEvents(season, year, course_anmalningskod):

    defaultLogger.info('Retrieving course events...')
    try:
        # Url string
        url = '/web/lnu/db1/schema1/s.json?object=courseevt_%s%s-%s&tab=3' % (str(season), str(year), str(course_anmalningskod))
        defaultLogger.info('URL: %s' % url)
        
        # HTTPS connection
        connection = httplib.HTTPSConnection('se.timeedit.net')
        defaultLogger.info('Connection: %s' % connection)
        
        # HTTP header
        header = {
            'Content-Type':'application/json; charset=UTF-8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent':'lnu-timeedit-app',
            'Vary':'Accept-Charset, Accept-Encoding, Accept-Language, Accept',
        }
        
        
        # Create the request
        connection.request('GET', url, {}, header)
        defaultLogger.info('Succes!')
        defaultLogger.info(' ')
        
        # Read the json data and create a python dict
        json_data = json.loads(connection.getresponse().read())
        
        # Pretty print it, only use thins when looking for all data
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json_data)
        
        event_list = []
        try:
            json_data['messages']
        except KeyError as e:
            print("Error here! Nothing dager!")
            pass
        
        try:
            for i in json_data['reservations']:
                
                data = {
                    'startdate':'',
                    'starttime':'',
                    'endtime':'',
                    'info':'',
                    'desc':'',
                    'room':'',
                    'teacher':'',
                }
                
                data['startdate'] = i['startdate']
                data['starttime'] = i['starttime']
                data['endtime'] = i['endtime']
                data['info'] = i['columns'][5]
                data['room'] = i['columns'][2]
                data['teacher'] = i['columns'][3]
                data['desc'] = i['columns'][8]

                event_list.append(data)

            return event_list
        
        except KeyError as e:
            pass
            
    except ValueError as e:
        pass

    
    
    return [{
        'startdate':'',
        'starttime':'',
        'endtime':'',
        'info':'This course is inactive.',
        'room':'',
        'desc':'',
        'teacher':'',
    },]


# This function returns a list
def getCourseId(course_code):
    # Try to connect
    defaultLogger.info('Requesting course id...')
    try:
        url = 'https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text='+course_code+'%20&types=5'
        #'https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text=1BD105%20&types=5'
        req = requests.get(url)

        defaultLogger.info('URL: %s' % url)
        defaultLogger.info('REQUEST: %s' % req)
        
        data = json.loads(req.text)
        try:
            data = data['records']

            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(data)

            course_code_list = []
            
            for course in data:
                # This sorts out 
                if (course['fields'][2]['values'][0] == __THIS_SEMESTER + __THIS_YEAR):
                    course_code_list.append(course['textId'])

            defaultLogger.info('Successfully retrieved course IDs!')
            defaultLogger.info(' ')
            
            return course_code_list
        
        except KeyError as e:
            defaultLogger.info(e)
            defaultLogger.info('Retrieving Course IDs failed due to KeyError Exception...')
            
            errorLogger.info('KeyError in timeedit_handler.getCourseId:')
            errorLogger.info(e)
            errorLogger.info(' ')
            
    except requests.exceptions.ConnectionError as e:
        defaultLogger.info(e)
        defaultLogger.info('Retrieving Course IDs failed due to ConnectionError Exception...')

        errorLogger.info('ConnectionError in timeedit_handler.getCourseId:')
        errorLogger.info(e)
        errorLogger.info(' ')

        
def getCourseInfo(course_id):
    
    defaultLogger.info('Requesting course information for course_id: %s...' % course_id)
    try:
        req = requests.get('https://se.timeedit.net/web/lnu/db1/schema2/objects/'+course_id+'/o.json')

        defaultLogger.info('REQUEST: %s' % req)
        
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(req.text)

        data = json.loads(req.text)

        data = json.dumps(data['records'])
        data = json.loads(data)
        data = data[0]['fields']
        data = data
        #pp.pprint(data)
        defaultLogger.info('Success!')
        defaultLogger.info(' ')
        
        return {
            'name':data[1]['values'][0],           
            'course_code':data[0]['values'][0],
            'course_id':course_id,
            #'vecka' (data[5]['values'][0])
            'course_reg':data[6]['values'][0][5:],
            'semester': __THIS_SEMESTER,
            'url': '',
            'year':__THIS_YEAR
        }
            

    except requests.exceptions.ConnectionError as e:
        defaultLogger.info(e)
        defaultLogger.info('Retrieving course info failed due to ConnectionError Exception...')
        
        errorLogger.info('ConnectionError in timeedit_handler.getCourseInfo:')
        errorLogger.info(e)
        errorLogger.info(' ')





    
