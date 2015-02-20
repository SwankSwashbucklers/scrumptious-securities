import urllib, urllib2, httplib
import json, re

class Stock(object):
	stock_data = {}
	endpoint   = ""

	def __init__(self, fields, ticker):
		self.stock_data['Ticker']  = ticker
		field_string = ""
		for f in range(0, len(fields)):
			self.stock_data[fields[f]] = ""
			field_string += fields[f]
			if (f < (len(fields)-1)):
				field_string += ", "

		sql_stmt = 'SELECT {f} FROM yahoo.finance.quotes WHERE symbol="{t}"'
		req_data                 = {}
		req_data['q']            = re.sub(r'\{f\}', field_string,
								   re.sub(r'\{t\}', ticker, sql_stmt))
		req_data['format']       = 'json'
		req_data['diagnostics']  = 'false'
		req_data['env']          = 'store://datatables.org/alltableswithkeys'
		req_data['callback']     = ''
		self.endpoint = 'https://query.yahooapis.com/v1/public/yql?' + urllib.urlencode(req_data)
		self.refresh_data()

	def make_request(self):
		try:
			return json.load(urllib2.urlopen(self.endpoint))
		except urllib2.HTTPError, e:
			print "HTTPError = " + str(e.code)
		except urllib2.URLError, e:
			print "URLError = " + str(e.reason)
		except httplib.HTTPException, e:
			print "HTTPException"
		except Exception:
			print "Unknown exception"
		return None

	def refresh_data(self):
		response = self.make_request()
		if response is None: 
			quote = None 
		else:
			quote = response['query']['results']['quote']
		
		for key in self.stock_data:
			if key == 'Ticker': continue
			if quote is None: 
				self.stock_data[key] = None 
			else:
				self.stock_data[key] = quote[key]


class TickerStock(Stock):
	name   = ""
	ticker = ""
	bid    = ""
	ask    = ""

	def __init__(self, ticker):
		fields = ['Name', 'Bid', 'Ask']
		super(TickerStock, self).__init__(fields, ticker)

	def refresh_data(self):
		super(TickerStock, self).refresh_data()
		if not (self.name):
			self.name = self.stock_data['Name']
		if not (self.ticker):
			self.ticker = self.stock_data['Ticker']
		self.bid = self.stock_data['Bid']
		self.ask = self.stock_data['Ask']

	def get_name_string(self):
		if (self.name):
			return self.name + ' (' + self.ticker + ')'
		return self.ticker

	def get_bid_string(self):
		if not self.bid is None:
			return " Bid : " + self.bid
		return " Bid : N/A"

	def get_ask_string(self):
		if not self.ask is None:
			return " Ask : " + self.ask
		return " Ask : N/A"

