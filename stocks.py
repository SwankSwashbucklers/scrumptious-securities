import urllib, urllib2
import json, re, math
import time, os
os.system('cls')

MAX_LENGTH   = 80
BUFFER       = 5
REFRESH_RATE = 2
WATCHLIST    = ['TSLA', 'GOOGL', 'GOOG']


class Stock:
	data     = {}
	url      = 'https://query.yahooapis.com/v1/public/yql'
	sql_stmt = 'SELECT Name, Bid, Ask, LastTradePriceOnly FROM yahoo.finance.quotes WHERE symbol="{}"'

	def __init__(self, ticker):
		self.ticker              = ticker
		self.data['q']           = re.sub(r'\{\}', ticker, self.sql_stmt)
		self.data['format']      = 'json'
		self.data['diagnostics'] = 'false'
		self.data['env']         = 'store://datatables.org/alltableswithkeys'
		self.data['callback']    = ''
		self.full_url = self.url + '?' + urllib.urlencode(self.data)
		self.refresh_data()

	def refresh_data(self):
		response  = json.load(urllib2.urlopen(self.full_url))
		# TODO: add error checking
		self.name = response['query']['results']['quote']['Name'] + ' (' + self.ticker + ')'
		self.bid  = response['query']['results']['quote']['Bid']
		self.ask  = response['query']['results']['quote']['Ask']


stocks = []
for ticker in WATCHLIST:
	stocks.append(Stock(ticker))

while (1):
	output  = []
	longest = 0

	for stock in stocks:
		stock.refresh_data()
		if (longest < len(stock.name)): 
			longest = len(stock.name)
		if (longest < len("Bid : " + stock.bid)): 
			longest = len("Bid : " + stock.bid)
		if (longest < len("Ask : " + stock.ask)): 
			longest = len("Ask : " + stock.ask)

	columns = int(math.floor(MAX_LENGTH/float(longest+BUFFER)))
	if ((columns*longest+(columns-1)*BUFFER) < MAX_LENGTH): 
		columns = columns + 1
	rows    = int(math.ceil(len(stocks)/float(columns)))

	for r in range(0, rows):
		for x in range(0, 3):
			output.append("")
		for c in range(0, columns):
			if ((r+1)*(c+1) > len(stocks)):
				break
			name_string = stocks[(r+1)*(c+1)-1].name
			bid_string  = "Bid : " + stocks[(r+1)*(c+1)-1].bid
			ask_string  = "Ask : " + stocks[(r+1)*(c+1)-1].ask
			output[((1)*(r+1))-1] += name_string
			output[((2)*(r+1))-1] += bid_string
			output[((3)*(r+1))-1] += ask_string
			if not (c==(columns-1)):
				for x in range(0, (longest-len(name_string))+BUFFER):
					output[((1)*(r+1))-1] += " "
				for x in range(0, (longest-len(bid_string))+BUFFER):
					output[((2)*(r+1))-1] += " "
				for x in range(0, (longest-len(ask_string))+BUFFER):
					output[((3)*(r+1))-1] += " "

	os.system('cls')
	for line in output:
		print line
	time.sleep(REFRESH_RATE)