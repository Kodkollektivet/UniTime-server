
import httplib
import requests
import pprint

print('Trying to get couses and course info')
# Not found
data = {'course':'1DV001'}
req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
print(req.text)

# Invalid input
data = {'course':'1DV0011111'}
req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
print(req.text)

# Success
data = {'course':'1DV008'}
req = requests.post('http://127.0.0.1:8001/api/course/', data=data)
print(req.text)

print('\n\nTrying to get events from a course')

# Success
data = {'course':'1DV008'}
req = requests.post('http://127.0.0.1:8001/api/event/', data=data)
print(req.text)
