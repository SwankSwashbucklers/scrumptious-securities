import urllib
import urllib2
import json
import time
import os

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
	os.system('cls')
	data = urllib2.urlopen(full_url)
	res = json.load(data)
	quote = res['query']['results']['quote']

	print quote['Name']
	print "Bid : " + quote['Bid']
	print "Ask : " + quote['Ask']
	time.sleep(10)

print res