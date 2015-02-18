import urllib, urllib2
import json, time, os
os.system('cls')

data = {}
data['q'] = 'SELECT Name, Bid, Ask, LastTradePriceOnly FROM yahoo.finance.quotes WHERE symbol="TSLA"'
data['format'] = 'json'
data['diagnostics'] = 'false'
data['env'] = 'store://datatables.org/alltableswithkeys'
data['callback'] = ''

url_values = urllib.urlencode(data)
url = 'https://query.yahooapis.com/v1/public/yql'
full_url = url + '?' + url_values

while (1):
	data = urllib2.urlopen(full_url)
	res = json.load(data)
	quote = res['query']['results']['quote']

	os.system('cls')
	print quote['Name']
	print "Bid : " + quote['Bid']
	print "Ask : " + quote['Ask']
	time.sleep(1)