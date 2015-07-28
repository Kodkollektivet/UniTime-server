# -*- coding: utf-8 -*-
# This file us used to find courses from LNU page and send POST requests to the API
# It is only the course code that is saved.
# This script can be a starting point to a service that is searching for course info all the time.
# At the time of writing this, we find around 4854 courses
# This takes about 80 minutes to request this courses
# This script will run every week.

import requests
import re
import json
import time

def getAllCourseCodes_scrapper(urls):

    for url in urls:
        req = requests.get(url)                                # the request
        match_code = re.compile(r'\(\d...\d.\)', re.M|re.I)   # the regexp
        all_courses = match_code.findall(req.text)             # find all of the course_anmalningskod
        all_courses = map(lambda x:x.strip('()'), all_courses) # strip away all of the ()

        for i in all_courses:
            data = {'code':i}
            req = requests.post('http://unitime.se/api/course_codes/', data=data)


urls = [
    'http://lnu.se/utbildning/kurser',
    'http://lnu.se/ekonomihogskolan/vara-program-och-kurser/kurser-pa-grundniva',
    'http://lnu.se/ekonomihogskolan/vara-program-och-kurser/kurser-pa-avancerad-niva',
    'http://lnu.se/ekonomihogskolan/vara-program-och-kurser/distanskurser',
    'http://lnu.se/fakulteten-for-konst-och-humaniora/utbildning/sommarkurser-2015',
]

getAllCourseCodes_scrapper(urls)


def getFromSomeAPI():
    url = "http://api.kursinfo.lnu.se/kurstillfallen/default.aspx/GetCompletionList"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {'prefixText':"","count":'10',"contextKey":"CourseCodes"}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    data = r.json()

    for i in data['d']:
        data = {'code':i}
        req = requests.post('http://unitime.se/api/course_codes/', data=data)


getFromSomeAPI()


def requestCourseInfo():
    req = requests.get('http://unitime.se/api/course_codes/')
    for i in req.json():
        data = {'course':i['code']}
        req = requests.post('http://unitime.se/api/course/', data=data)
        time.sleep(1)

requestCourseInfo()


