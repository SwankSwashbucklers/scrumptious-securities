import urllib, urllib2
import json, re, math
import time, os
os.system('cls')

MAX_LENGTH   = 80
H_BUFFER     = 2
V_BUFFER     = 4
REFRESH_RATE = 2
WATCHLIST    = ['TSLA', 'GOOGL', 'GOOG', 'AAPL', 'OMCL', 'AAL', 'GPRO']


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
		self.name = response['query']['results']['quote']['Name']
		self.bid  = response['query']['results']['quote']['Bid']
		self.ask  = response['query']['results']['quote']['Ask']

	def get_name_string(self):
		return self.name + ' (' + self.ticker + ')'

	def get_bid_string(self):
		return "Bid : " + self.bid

	def get_ask_string(self):
		return "Ask : " + self.ask


stocks = []
for ticker in WATCHLIST:
	stocks.append(Stock(ticker))

while (1):
	output  = []
	longest = 0

	for stock in stocks:
		stock.refresh_data()
		if (longest < len(stock.get_name_string())): 
			longest = len(stock.get_name_string())
		if (longest < len(stock.get_bid_string())): 
			longest = len(stock.get_bid_string())
		if (longest < len(stock.get_ask_string())): 
			longest = len(stock.get_ask_string())

	columns = int(math.floor(MAX_LENGTH/float(longest+H_BUFFER)))
	#if ((columns*longest+(columns-1)*H_BUFFER) < MAX_LENGTH): 
	#	columns = columns + 1
	rows    = int(math.ceil(len(stocks)/float(columns)))

	for r in range(0, rows):
		for x in range(0, 3):
			output.append("")
		for c in range(0, columns):
			if (c+(r*columns) >= len(stocks)):
				break
			stock = stocks[c+(r*columns)]
			output[(0)+(r*3)] += stock.get_name_string()
			output[(1)+(r*3)] += stock.get_bid_string()
			output[(2)+(r*3)] += stock.get_ask_string()
			if not (c==(columns-1)):
				for x in range(0, (longest-len(stock.get_name_string()))+H_BUFFER):
					output[(0)+(r*3)] += " "
				for x in range(0, (longest-len(stock.get_bid_string()))+H_BUFFER):
					output[(1)+(r*3)] += " "
				for x in range(0, (longest-len(stock.get_ask_string()))+H_BUFFER):
					output[(2)+(r*3)] += " "

	os.system('cls')
	for l in range(0, len(output)):
		if (l % 3 == 0) and not (l == 0):
			for x in range(0, V_BUFFER):
				print ""
		print output[l]
	time.sleep(REFRESH_RATE)