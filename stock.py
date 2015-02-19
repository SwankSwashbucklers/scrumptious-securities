import urllib, urllib2, httplib
import json, re

class Stock:
	data     = {}
	name     = ""
	bid      = ""
	ask      = ""
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
		try:
			response  = json.load(urllib2.urlopen(self.full_url))
			if not (self.name):
				self.name = response['query']['results']['quote']['Name']
			self.bid  = response['query']['results']['quote']['Bid']
			self.ask  = response['query']['results']['quote']['Ask']
		except urllib2.HTTPError, e:
			print "HTTPError = " + str(e.code)
		except urllib2.URLError, e:
			print "URLError = " + str(e.reason)
		except httplib.HTTPException, e:
			print "HTTPException"
		except Exception:
			print "Unknown exception"

	def get_name_string(self):
		if (self.name):
			return self.name + ' (' + self.ticker + ')'
		return self.ticker

	def get_bid_string(self):
		if (self.bid):
			return " Bid : " + self.bid
		return " Bid : N/A"

	def get_ask_string(self):
		if (self.ask):
			return " Ask : " + self.ask
		return " Ask : N/A"