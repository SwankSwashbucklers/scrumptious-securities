import urllib, urllib2, httplib
import json, re

class Stock(object):
	stock_data = {}
	req_data   = {}
	url        = 'https://query.yahooapis.com/v1/public/yql'
	sql_stmt   = 'SELECT {f} FROM yahoo.finance.quotes WHERE symbol="{t}"'

	def __init__(self, fields, ticker):
		field_string = ""
		for f in range(0, len(fields)):
			self.stock_data[fields[f]] = ""
			field_string += fields[f]
			if (f < (len(fields)-1)):
				field_string += ", "

		self.ticker                    = ticker
		self.req_data['q']             = re.sub(r'\{f\}', field_string,
										 re.sub(r'\{t\}', ticker, self.sql_stmt))
		self.req_data['format']        = 'json'
		self.req_data['diagnostics']   = 'false'
		self.req_data['env']           = 'store://datatables.org/alltableswithkeys'
		self.req_data['callback']      = ''
		self.full_url = self.url + '?' + urllib.urlencode(self.req_data)
		self.refresh_data()

	def make_request(self):
		try:
			return json.load(urllib2.urlopen(self.full_url))
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
			if quote is None: 
				self.stock_data[key] = None 
			else:
				self.stock_data[key] = quote[key]


class TickerStock(Stock):
	name = ""
	bid  = ""
	ask  = ""

	def __init__(self, ticker):
		fields = ['Name', 'Bid', 'Ask']
		super(TickerStock, self).__init__(fields, ticker)

	def refresh_data(self):
		super(TickerStock, self).refresh_data()
		if not (self.name):
			self.name = self.stock_data['Name']
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

