# -*- coding:utf-8 -*-

import httplib
import json
import pprint
import requests
import re
import datetime

__THISYEAR = datetime.datetime.now().strftime('%y')

# course here is Anmälningskod
# season is VT or HT
# year is __THISYEAR
def getCourseData(season, year, course):

    try:
        # Url string
        url = '/web/lnu/db1/schema1/s.json?object=courseevt_%s%s-%s&tab=3' % (str(season), str(year), str(course))
        print(url)
        #url = '/web/lnu/db1/schema1/s.json?object=courseevt_VT15-%s&tab=3' % course        

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
        pp.pprint(json_data['reservations'])
        
        for i in json_data['reservations']:
            print('Start date: '+ i['startdate'])
            print('Start time: '+ i['starttime'])
            print('End time: '+ i['endtime'])
            print('Info: ' + i['columns'][5])
            print('Room: ' + i['columns'][2])
            print('Teacher: ' + i['columns'][3])
            
            
    except ValueError as e:
        print(e)
        print('terminating......')
        quit

# Simple page scrapper
# looking for Anmälningskod and if its Vår och Höst (HT / VT)
def getSimpleRequests(course):
    # send the request with couser ex 1DV008
    req = requests.get('http://lnu.se/utbildning/kurser/%s' % course)

    # see if anmälningskod is in the page
    match_code = re.search(r'LNU-\d\d\d\d\d', req.text, )

    # see if Vår is in the page
    match_season_var = re.search(r'V.r', req.text)

    # see if Höst is in the page
    match_season_host = re.search(r'H.st', req.text)

    # if matches
    if match_code:
        print(match_code.group())
        if match_season_host:
            print('Höst found')
            print('calling getCourseData()......')
            getCourseData('HT', __THISYEAR, match_code.group()[4:])
        if match_season_var:
            print('Vår found')
            getCourseData('VT', __THISYEAR, match_code.group()[4:])
    else:
        print(course+' not found')
            
    
getSimpleRequests('1MA162')

