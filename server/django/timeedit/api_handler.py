# -*- coding:utf-8 -*-

# Links that does not work
# http://lnu.se/utbildning/kurser/1MA164

import httplib
import json
import pprint
import requests
import re
import datetime

__THISYEAR = datetime.datetime.now().strftime('%y')
__THIS_SEMESTER = ''
__MONTH_NOW = int(datetime.datetime.now().strftime('%m'))


# Evaluate if now() is HT or VT
if (__MONTH_NOW <= 6):
    __THIS_SEMESTER = 'VT'
else:
    __THIS_SEMESTER = 'HT'

    
# course here is Anmälningskod
# season is VT or HT
# year is __THISYEAR
def getCourseEvents(season, year, course_anmalningskod):

    try:
        # Url string
        url = '/web/lnu/db1/schema1/s.json?object=courseevt_%s%s-%s&tab=3' % (str(season), str(year), str(course_anmalningskod))

        # HTTPS connection
        connection = httplib.HTTPSConnection('se.timeedit.net')

        # HTTP header
        header = {
            'Content-Type':'application/json; charset=UTF-8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent':'lnu-timeedit-app',
            'Vary':'Accept-Charset, Accept-Encoding, Accept-Language, Accept',
        }

        # Create the request
        connection.request('GET', url, {}, header)

        # Read the json data and create a python dict
        json_data = json.loads(connection.getresponse().read())

        # Pretty print it, only use thins when looking for all data
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json_data['messages'])

        event_list = []
        try:
            json_data['messages']
        except KeyError as e:
            pass

        try:
            for i in json_data['reservations']:

                data = {
                    'startdate':'',
                    'starttime':'',
                    'endtime':'',
                    'info':'',
                    'room':'',
                    'teacher':'',
                }
                
                data['startdate'] = i['startdate']
                data['starttime'] = i['starttime']
                data['endtime'] = i['endtime']
                data['info'] = i['columns'][5]
                data['room'] = i['columns'][2]
                data['teacher'] = i['columns'][3]                            
                event_list.append(data)
            return event_list
        
        except KeyError as e:
            pass
            
    except ValueError as e:
        pass
    
    return [{
        'startdate':'Not found',
        'starttime':'Not found',
        'endtime':'Not found',
        'info':'Not found',
        'room':'Not found',
        'teacher':'Not found',
    },]


# Simple page scrapper
# looking for Anmälningskod and if its Vår och Höst (HT / VT)
def getCourseInfo(course):
    # send the request with couser ex 1DV008
    url = 'http://lnu.se/utbildning/kurser/%s#semseter_20%s1' % (course, __THIS_SEMESTER) 
    req = requests.get(url)

    # see if anmälningskod is in the page
    match_code = re.search(r'LNU-\d\d\d\d\d', req.text)

    # if matches
    if match_code:
        return {
            'course_code':course,
            'course_anmalningskod':match_code.group()[4:],
            'season': __THIS_SEMESTER,
            'html_url':url,
            'year':__THISYEAR,
        }

    else:
        print(course+' not found')
            

#This work like public static void main in Java
if __name__ == '__main__':
    course = getCourseInfo('1BD101')
    print(getCourseEvents(course['season'], course['year'], course['course_anmalningskod']))
