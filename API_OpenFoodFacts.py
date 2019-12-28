import requests
payload = {'search_terms': 'riz','purchase_place': 'strasbourg', 'action': 'process','page_size': 10,'page': 2, 'json': 1}
headers = {'User-Agent': 'python-requests/2.22.0'}
r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', headers = headers, params = payload)
print(r)
print(r.url)

with open('response_API.txt', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)