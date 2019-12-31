import urllib.request

x = urllib.request.urlopen('https://fr.openfoodfacts.org/cgi/search.pl?search_terms=pizzas&action=process&page_size=10&page=2&json=1')
print(x.read())