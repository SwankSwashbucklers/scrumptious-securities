import urllib, urllib2
import re

#http://finance.yahoo.com/q?s=aapl
class Stock(object):
	value = 0.0
	name  = ""
	def __init__(self, ticker):
		data = {}
		data['s'] = ticker.lower()
		full_url = 'http://finance.yahoo.com/q?' + urllib.urlencode(data)
		response = urllib2.urlopen(full_url).read()
		self.value = float(
			str(re.search(r'[0-9\.]*$', 
			str(re.search(r'<span class="time_rtq_ticker"><span[\w\s="]*>[\w\s\.]*', response).group())).group()))
		self.name = str(re.search(r'(?<=: Summary for ).*(?=-)', 
			str(re.search(r'(?<=<title>).*(?=<\/title>)', response).group())).group())

		
apple = Stock('AAPL')
tesla = Stock('TSLA')
print apple.name
print apple.value
print tesla.name
print tesla.value
