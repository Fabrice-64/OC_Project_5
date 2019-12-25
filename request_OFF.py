import requests
import json
link = 'https://world.openfoodfacts.org'
headers = {'User-Agent': 'Fabrice-64, Mozilla, Version 5.0'}
payload = {'country': 'fr', 'json': 1, 'page_size' : '1000', 'page' : '1'}
response = requests.get(url = link, headers = headers, params = payload)
filename = 'data_from_OFF.txt'
print(response)
print(response.url)
with open(filename, 'wb') as fd:
    for chunk in response.iter_content(1000):
        fd.write(chunk)