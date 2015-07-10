
# This file us used to find courses from LNU page and add them to database
# It is only the course code that is saved.
# This script can be a starting point to a service that is searching for course info all the time.

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

import httplib
import requests
import re
import json

from timeedit.models import CourseCodes

from django.db.utils import IntegrityError


def getAllCourseCodes_scrapper(urls):
    for url in urls:

        req = requests.get(url)                                # the request
        match_code = re.compile(r'\(\d...\d.\)', re.M|re.I)   # the regexp
        all_courses = match_code.findall(req.text)             # find all of the course_anmalningskod
        all_courses = map(lambda x:x.strip('()'), all_courses) # strip away all of the ()

        for i in all_courses:
            try:
                course = CourseCodes(code=i.upper())
                course.save()
                print(str(i)+' saved')

            except TypeError:
                print('TypeError')

            except IntegrityError as e:
                print(e)
                pass

            except UnicodeEncodeError as e:
                print(e)
                pass

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
        try:
            course = CourseCodes(code=i.upper())
            course.save()
            print(str(i)+' saved')

        except TypeError:
            print('TypeError')

        except IntegrityError as e:
            print(e)
            pass

        except UnicodeEncodeError as e:
            print(e)
            pass


getFromSomeAPI()