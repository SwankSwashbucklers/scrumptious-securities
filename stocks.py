import urllib, urllib2
import json, re, time, os
os.system('cls')


class Stock:
	data     = {}
	url      = 'https://query.yahooapis.com/v1/public/yql'
	sql_stmt = 'SELECT Name, Bid, Ask, LastTradePriceOnly FROM yahoo.finance.quotes WHERE symbol="{}"'

	def __init__(self, ticker):
		self.data['q']           = re.sub(r'\{\}', ticker, self.sql_stmt)
		self.data['format']      = 'json'
		self.data['diagnostics'] = 'false'
		self.data['env']         = 'store://datatables.org/alltableswithkeys'
		self.data['callback']    = ''
		self.full_url = self.url + '?' + urllib.urlencode(self.data)
		self.refresh_data()

	def refresh_data(self):
		response  = json.load(urllib2.urlopen(self.full_url))
		self.name = response['query']['results']['quote']['Name']
		self.bid  = response['query']['results']['quote']['Bid']
		self.ask  = response['query']['results']['quote']['Ask']

tesla = Stock('TSLA');

while (1):
	tesla.refresh_data()
	os.system('cls')
	print tesla.name
	print "Bid : " + tesla.bid
	print "Ask : " + tesla.ask
	time.sleep(1)