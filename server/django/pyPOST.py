# -*- coding:utf-8 -*-

print('öäå')

import httplib
import requests
import pprint
import json
import datetime

__THIS_YEAR = datetime.datetime.now().strftime('%y')
__THIS_SEMESTER = ''
__MONTH_NOW = int(datetime.datetime.now().strftime('%m'))


# Evaluate if now() is HT or VT
if (__MONTH_NOW <= 6):
    __THIS_SEMESTER = 'VT'
else:
    __THIS_SEMESTER = 'HT'


# Important links
#https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text=1DV008&types=5&fe=30.V%25C3%25A4xj%25C3%25B6

# ---------------------------------------- TESTING OUT INTERNAL API -----------------------------------

# print('Trying to get couses and course info')
# # Not found
# data = {'course':'1DV001'}
# req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
# print(req.text)

# # Invalid input
# data = {'course':'1DV0011111'}
# req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
# print(req.text)

# # Success
# data = {'course':'1DV008'}
# req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
# print(req.text)

# print('\n\nTrying to get events from a course')

# # Success
# data = {'course':'1DV008'}
# req = requests.post('http://127.0.0.1:8001/api/event/', data=data)
# print(req.text)

# ------------------------------------- INTERNAL TESTING ENDS ------------------------------------------


# -------------------------------------- DATA COLLECTION FROM LNUs SITES/TIMEEDIT -------------------------
# This request gives us the unique id, a strange number
# It also give other info, like course name and stuff like that
# 1GN214



def getCourseInfo_api(course_code):

    req = requests.get('https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text='+course_code+'%20&types=5')
    data = json.loads(req.text)
    data = data['records']

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data[0])

    for course in data:
        if (course['fields'][2]['values'][0] == __THIS_SEMESTER+__THIS_YEAR):
            pass
            
            
    


# req = requests.get('https://se.timeedit.net/web/lnu/db1/schema2/objects/110303/o.json')
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json.loads(req.text))



getCourseInfo('1DV008')
#getCourseInfo('1GN214')


