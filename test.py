class ClassA(object):
	"""docstring for ClassA"""
	def __init__(self, *args):
		print "Init Class A" 
		super(ClassA, self).__init__()
		print "Post Class A" 
		
		
		

class ClassB(object):
	"""docstring for ClassB"""
	def __init__(self, *args):
		print "Init Class B"
		super(ClassB, self).__init__()
		print "Post Class B" 
		



class ClassC(ClassA, ClassB):
	"""docstring for ClassC"""
	def __init__(self, *args):
		print "Init Class C"
		super(ClassC, self).__init__(*args)
		print "Post Class C" 
		



test = ClassC(6)
		
		
		
import urllib, urllib2, httplib
import json, re

class Stock(object):
	def __init__(self, endpoint):
		super(Stock, self).__init__()
		self.endpoint = endpoint

	def make_request(self):
		try:
			return urllib2.urlopen(self.endpoint)
		except urllib2.HTTPError, e:
			print "HTTPError = " + str(e.code)
		except urllib2.URLError, e:
			print "URLError = " + str(e.reason)
		except httplib.HTTPException, e:
			print "HTTPException"
		except Exception:
			print "Unknown exception"
		return None



class Scraper_Stock(Stock):
	def __init__(self, ticker):
		req_data = {}
		req_data['s'] = ticker.lower()
		endpoint = 'http://finance.yahoo.com/q?' + urllib.urlencode(req_data)
		super(Stock, self).__init__(endpoint)

		self.scraped_data = {}
		self.scraped_data['Name']  = ""
		self.scraped_data['Value'] = 0.0
		self.refresh_value()

	def refresh_value(self): #TODO: add checking if regex cant find match
		resp = self.make_request()
		if resp is None: 
			return
		response = resp.read() 

		self.scraped_data['Value'] = float(
			str(re.search(r'[0-9\.]*$', 
			str(re.search(r'<span[\w\s="]*class="time_rtq_ticker[\w\s="]*><span[\w\s="]*>[\w\s\.]*', response).group())).group()))

		if not (self.scraped_data['Name']):
			self.scraped_data['Name'] = str(re.search(r'(?<=: Summary for ).*(?=-)', 
				str(re.search(r'(?<=<title>).*(?=<\/title>)', response).group())).group())



class YQL_Stock(Stock):
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

	def refresh_data(self):
		response = self.make_yql_request()
		if response is None: 
			return
		quote = json.load(response)['query']['results']['quote']
		
		for key in self.stock_data:
			if key == 'Ticker': 
				continue
			self.stock_data[key] = quote[key]