# -*- coding: utf-8 -*-
import urllib, urllib2, httplib
import json, re

class Scraper_Stock(object):
	scraped_data = {}
	endpoint     = ""

	def __init__(self, ticker):
		self.setup(ticker)

	def setup(self, ticker):
		req_data = {}
		req_data['s'] = ticker.lower()
		self.endpoint = 'http://finance.yahoo.com/q?' + urllib.urlencode(req_data)

		self.scraped_data['Name']  = ""
		self.scraped_data['Value'] = 0.0
		self.refresh_value()

	def make_request(self):
		try:
			return urllib2.urlopen(self.endpoint).read()
		except urllib2.HTTPError, e:
			print "HTTPError = " + str(e.code)
		except urllib2.URLError, e:
			print "URLError = " + str(e.reason)
		except httplib.HTTPException, e:
			print "HTTPException"
		except Exception:
			print "Unknown exception"
		return None

	def refresh_value(self): #TODO: add checking if regex cant find match
		response = self.make_request()
		if response is None:
			return

		self.scraped_data['Value'] = float(
			str(re.search(r'[0-9\.]*$', 
			str(re.search(r'<span[\w\s="]*class="time_rtq_ticker[\w\s="]*><span[\w\s="]*>[\w\s\.]*', response).group())).group()))

		if not (self.scraped_data['Name']):
			self.scraped_data['Name'] = str(re.search(r'(?<=: Summary for ).*(?=-)', 
				str(re.search(r'(?<=<title>).*(?=<\/title>)', response).group())).group())



class YQL_Stock(object):
	stock_data     = {}
	yql_endpoint   = ""

	def __init__(self, fields, ticker):
		self.yql_setup(fields, ticker)

	def yql_setup(self, fields, ticker):
		field_string = ""
		for f in range(0, len(fields)):
			self.stock_data[fields[f]] = None
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
		self.yql_endpoint = 'https://query.yahooapis.com/v1/public/yql?' + urllib.urlencode(req_data)
		self.refresh_data()

	def make_yql_request(self):
		try:
			return json.load(urllib2.urlopen(self.yql_endpoint))
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
		response = self.make_yql_request()
		if response is None: 
			quote = None 
		else:
			quote = response['query']['results']['quote']
		
		for key in self.stock_data:
			if key == 'Ticker': 
				continue
			if not quote is None: 
				self.stock_data[key] = quote[key]



class TickerStock(Scraper_Stock, YQL_Stock):
	name           = ""
	ticker         = ""
	value          = 0.0
	previous_close = 0.0
	open_price     = 0.0

	def __init__(self, ticker):
		self.ticker = ticker
		fields = ['PreviousClose', 'Open']
		super(TickerStock, self).setup(ticker)
		super(TickerStock, self).yql_setup(fields, ticker)

	def refresh_value(self):
		super(TickerStock, self).refresh_value()
		if not (self.name):
			self.name = self.scraped_data['Name']
		self.value = self.scraped_data['Value']

	def refresh_data(self):
		super(TickerStock, self).refresh_data()
		self.previous_close = float(self.stock_data['PreviousClose'])
		self.open_price     = float(self.stock_data['Open'])

	def get_name_string(self):
		if (self.name):
			return self.name + ' (' + self.ticker + ')'
		return self.ticker

	def get_value_string(self):
		if (self.value):
			if (self.previous_close):
				if (self.value > self.previous_close):
					dir_string = "\x1E"
				elif (self.value < self.previous_close):
					dir_string = "\x1F"
				else:
					dir_string = "\xFE"
				percent = ((self.value - self.previous_close)/self.previous_close)*100
				percent_string = '%.3f' % percent
			else:
				dir_string = "\xF9"
				percent_string = "--.---"
			value_string = '%.2f' % self.value
			return " " + value_string + " " + dir_string + " " + percent_string + " %"
		return " " + "N/A"

