
import httplib
import requests
import pprint


data = {'course':'1DV001'}

req = requests.post('http://127.0.0.1:8001/api/course/', data=data)

print(req.text)
