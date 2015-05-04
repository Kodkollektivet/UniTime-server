
import httplib
import requests
import pprint

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
