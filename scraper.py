import urllib, urllib2
import re

#http://finance.yahoo.com/q?s=aapl
class Stock(object):
	value = 0.0
	def __init__(self, ticker):
		data = {}
		data['s'] = ticker.lower()
		full_url = 'http://finance.yahoo.com/q?' + urllib.urlencode(data)
		response = urllib2.urlopen(full_url).read()
		m1 = re.search(r'<span class="time_rtq_ticker"><span[\w\s="]*>[\w\s\.]*', response)
		m = re.search(r'[0-9\.]*$', str(m1.group()))
		self.value = float(m.group())

apple = Stock('AAPL')
tesla = Stock('TSLA')
print apple.value
print tesla.value