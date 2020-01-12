import requests
import json
import config

OFF_page = 1
#payload = {'search_terms': config.categories[3],'json': 1, 'action' : "process", \
 #   'fields' : "brands,product_name,code,stores,nutrition_grade_fr","page_size": 1000, "page": OFF_page}
headers = {'User-Agent': 'python-requests/2.22.0'}
r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?action=display&tagtype_0=nova_groups&tag_contains_0=contains&tag_0=1&tagtype_1=categories&tag_contains_1=contains&tag_1=viandes&tagtype_2=nutrition_grades&tag_contains_2=contains&tag_2=A&sort_by=unique_scans_n&page_size=20&axis_x=energy&axis_y=products_n&action=display', headers = headers)

print(r)
print(r.url)
print(r.headers)
data = r.json()


print(type(data))
print(type(data['products']))