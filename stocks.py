import urllib, urllib2
import json, re, time, os
os.system('cls')

MAX_LENGTH = 200
WATCHLIST  = ['TSLA', 'GOOGL', 'GOOG']


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


stocks = []
for ticker in WATCHLIST:
	stocks.append(Stock(ticker))

while (1):
	line1 = ""
	line2 = ""
	line3 = ""
	for stock in stocks:
		stock.refresh_data()
		line1 = line1 + " " + stock.name
		line2 = line2 + " Bid : " + stock.bid
		line3 = line3 + " Ask : " + stock.ask

	os.system('cls')
	print line1
	print line2
	print line3
	time.sleep(1)