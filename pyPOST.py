# -*- coding:utf-8 -*-

import httplib
import requests
import pprint
import json
import datetime

__THIS_YEAR = datetime.datetime.now().strftime('%y')
__THIS_SEMESTER = ''
__MONTH_NOW = int(datetime.datetime.now().strftime('%m'))
__WEEK_NOW = datetime.datetime.now().isocalendar()[1]

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

# print('\n\nTrying to get events from a course...........')

# # Only one course in database on this course
# data = {'course':'4EN006'}
# req = requests.post('http://127.0.0.1:8001/api/event/', data=data)
# print(req.text.encode('utf-8'))

# # More than one item in the database
# data = {'course':'1DV008'}
# req = requests.post('http://127.0.0.1:8001/api/event/', data=data)
# print(req.text.encode('utf-8'))

# # If course does not exists
# data = {'course':'1DV000'}
# req = requests.post('http://127.0.0.1:8001/api/event/', data=data)
# print(req.text.encode('utf-8'))

# # Course info
# data = {'course':'1DV008'}
# req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
# print(req.text.encode('utf-8'))

# data = {'course':'4EN006'}
# req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
# print(req.text.encode('utf-8'))

# lista = ['1BD105',
# #          '2DI307',
# #          '1EN125',
# #          '1JA011',
# #          '1HI340',
# #          '1LI104',
# #          '1DV008',
# #          '1MU338',
# #          '1RK015',
#           ]
# #
# for i in lista:
#     data = {'course':i}
#     req = requests.post('http://127.0.0.1:8000/api/event/', data=data)
#     #req = requests.head('http://127.0.0.1:8001/api/course/')
#     #print(req.text.encode('utf-8'))
#
#     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(json.loads(req.text.encode('utf-8')))
#     print(req.headers)

import re
def getAllCourseCodes_scrapper(urls):
    for url in urls:
        #url = 'http://lnu.se/utbildning/kurser'
        req = requests.get(url)                                # the request
        # see if anmälningskod is in the page
        match_code = re.compile(r'\(\d...\d\d\)', re.M|re.I)   # the regexp
        all_courses = match_code.findall(req.text)             # find all of the course_anmalningskod
        all_courses = map(lambda x:x.strip('()'), all_courses) # strip away all of the ()


        # data = {'course':all_courses[0]}
        # print(data)
        # req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
        # print(req.text.encode('utf-8'))
        # print(req.headers)
        # print(req.status_code)
        for i in all_courses:
            try:
                #print(i)
                data = {'course':i}
                req = requests.post('http://unitime.se/api/course/', data=data)
                #print(req.text.encode('utf-8'))
                print(req.status_code, i)
            except TypeError:
                print('TypeError')
            # except UnicodeEncodeError:
            #     raw_input('')
            #     print(i)

urls = [
    'http://lnu.se/utbildning/kurser',
    'http://lnu.se/ekonomihogskolan/vara-program-och-kurser/kurser-pa-grundniva',
    'http://lnu.se/ekonomihogskolan/vara-program-och-kurser/kurser-pa-avancerad-niva',
    'http://lnu.se/ekonomihogskolan/vara-program-och-kurser/distanskurser',
    'http://lnu.se/fakulteten-for-konst-och-humaniora/utbildning/sommarkurser-2015',
]

#getAllCourseCodes_scrapper(urls)

# req = requests.get('http://api.kursinfo.lnu.se/kurstillfallen/')
# for key, value in req.cookies.items():
#     print (key, value)


# GET request
# r = requests.get('http://api.kursinfo.lnu.se/kurstillfallen/default.aspx')
# print(r.cookies)
# print(r.headers)
# print(r.status_code)




cookies = {'ASP.NET_SessionId': 'ajqhtwmmjcvef1jdiaktw22k',
           '__utma':"76804746.1228965635.1430113672.1430113672.1430113672.1",
           '__utmz' :"76804746.1430113672.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided)",
           '_ga':"GA1.2.1228965635.1430113672",
           }

data = {'prefixText':"1d","count":'10',"contextKey":"CourseCodes"}
headers = {
    #'Host': 'api.kursinfo.lnu.se',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json; charset=utf-8',
    #'Referer': 'http://api.kursinfo.lnu.se/kurstillfallen/default.aspx',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

headers1 = {
    'Origin': 'chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'sv-SE,sv;q=0.8,en-US;q=0.6,en;q=0.4',
}
# req = requests.post('http://api.kursinfo.lnu.se/kurstillfallen/default.aspx/GetCompletionList', data=data, headers=headers1)
# print(req.text.encode('utf-8'))
# print(req.headers)
# print(req.status_code)


import requests
import json

url = "http://api.kursinfo.lnu.se/kurstillfallen/default.aspx/GetCompletionList"
headers = {"content-type": "application/json; charset=UTF-8"}
payload = {'prefixText':"","count":'10',"contextKey":"CourseCodes"}
r = requests.post(url, headers=headers, data=json.dumps(payload))
data = r.json()

f = open('courses.txt', 'w')
lista = []
bra = 0
bad = 0
for i in data['d']:
    try:
        lista.append(i)
        f.write(repr(str(i)))
        f.write('\n')
        print(i)
        bra = bra + 1
    except UnicodeEncodeError:
        bad = bad + 1

f.close()
print(bra)
print(bad)

print(len(lista))

for i in lista:
    data = {'course':i}
    req = requests.post('http://127.0.0.1:8000/api/course/', data=data)
    print(req.status_code, i)


# req = requests.get('http://unitime.se/api/course/')
# print(req.text.encode('utf-8'))
# pp.pprint(req.headers)
# pp.pprint(req.status_code)

# ------------------------------------- INTERNAL TESTING ENDS ------------------------------------------


# -------------------------------------- DATA COLLECTION FROM LNUs SITES/TIMEEDIT -------------------------
# This request gives us the unique id, a strange number
# It also give other info, like course name and stuff like that
# 1GN214


# # This function returns a list
# def getCourseId(course_code):
#     # Try to connect
#     try:
#         req = requests.get('https://se.timeedit.net/web/lnu/db1/schema2/objects.txt?max=15&fr=t&partajax=t&im=f&sid=6&l=en_US&search_text='+course_code+'%20&types=5')
#         data = json.loads(req.text)
#         try:
#             data = data['records']

#             # pp = pprint.PrettyPrinter(indent=4)
#             # pp.pprint(data)

#             course_code_list = []
            
#             for course in data:
#                 # This sorts out 
#                 if (course['fields'][2]['values'][0] == __THIS_SEMESTER + __THIS_YEAR):
#                     course_code_list.append(course['textId'])

#             return course_code_list
        
#         except KeyError as e:
#             # LOG THIS ERROR
#             print('Error in: '),
#             print(e)
                
#     except requests.exceptions.ConnectionError as e:
#         # LOG THIS ERROR
#         print(e)
    
# def getCourseInfo(course_id):
#     try:
#         req = requests.get('https://se.timeedit.net/web/lnu/db1/schema2/objects/'+course_id+'/o.json')
#         pp = pprint.PrettyPrinter(indent=4)
#         #pp.pprint(req.text)

#         data = json.loads(req.text)

#         data = json.dumps(data['records'])
#         data = json.loads(data)
#         data = data[0]['fields']
#         data = data
#         #pp.pprint(data)

#         return {
#             'name':data[1]['values'][0],           
#             'course_code':data[0]['values'][0],
#             'course_id':course_id,
#             #'vecka' (data[5]['values'][0])
#             'course_reg':data[6]['values'][0][5:],
#             'semester': __THIS_SEMESTER,
#             'url': '',
#             'year':__THIS_YEAR
#         }
            

#     except requests.exceptions.ConnectionError as a:
#         # LOG THIS
#         print(e)

# #print(getCourseId('1GN214'))
# #print(getCourseId('1DV008'))

# print(getCourseInfo('110546'))
# print('')
# getCourseInfo('110303')



