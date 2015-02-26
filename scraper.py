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


apple  = Stock('AAPL')
tesla  = Stock('TSLA')
google = Stock('GOOGL')
print apple.name  + "          |  " + str(apple.value)
print tesla.name  + "  |  "         + str(tesla.value)
print google.name + "         |  "  + str(google.value)
print
print "\x1E"
print "\xFE"#"\xF9"   #"\x16"
print "\x1F"

#print "\x00" + "\x01" + "\x02" + "\x03" + "\x04" + "\x05" + "\x06" + "\x07"
#print "\x08" + "\x09" + "\x0A" + "\x0B" + "\x0C" + "\x0D" + "\x0E" + "\x0F"

#print "\x10" + "\x11" + "\x12" + "\x13" + "\x14" + "\x15" + "\x16" + "\x17"
#print "\x18" + "\x19" + "\x1A" + "\x1B" + "\x1C" + "\x1D" + "\x1E" + "\x1F"

#print "\x20" + "\x21" + "\x22" + "\x23" + "\x24" + "\x25" + "\x26" + "\x27"
#print "\x28" + "\x29" + "\x2A" + "\x2B" + "\x2C" + "\x2D" + "\x2E" + "\x2F"

#print "\x30" + "\x31" + "\x32" + "\x33" + "\x34" + "\x35" + "\x36" + "\x37"
#print "\x38" + "\x39" + "\x3A" + "\x3B" + "\x3C" + "\x3D" + "\x3E" + "\x3F"

#print "\x40" + "\x41" + "\x42" + "\x43" + "\x44" + "\x45" + "\x46" + "\x47"
#print "\x48" + "\x49" + "\x4A" + "\x4B" + "\x4C" + "\x4D" + "\x4E" + "\x4F"

#print "\x50" + "\x51" + "\x52" + "\x53" + "\x54" + "\x55" + "\x56" + "\x57"
#print "\x58" + "\x59" + "\x5A" + "\x5B" + "\x5C" + "\x5D" + "\x5E" + "\x5F"

#print "\x60" + "\x61" + "\x62" + "\x63" + "\x64" + "\x65" + "\x66" + "\x67"
#print "\x68" + "\x69" + "\x6A" + "\x6B" + "\x6C" + "\x6D" + "\x6E" + "\x6F"

#print "\x70" + "\x71" + "\x72" + "\x73" + "\x74" + "\x75" + "\x76" + "\x77"
#print "\x78" + "\x79" + "\x7A" + "\x7B" + "\x7C" + "\x7D" + "\x7E" + "\x7F"

#print "\x80" + "\x81" + "\x82" + "\x83" + "\x84" + "\x85" + "\x86" + "\x87"
#print "\x88" + "\x89" + "\x8A" + "\x8B" + "\x8C" + "\x8D" + "\x8E" + "\x8F"

#print "\x90" + "\x91" + "\x92" + "\x93" + "\x94" + "\x95" + "\x96" + "\x97"
#print "\x98" + "\x99" + "\x9A" + "\x9B" + "\x9C" + "\x9D" + "\x9E" + "\x9F"

#print "\xA0" + "\xA1" + "\xA2" + "\xA3" + "\xA4" + "\xA5" + "\xA6" + "\xA7"
#print "\xA8" + "\xA9" + "\xAA" + "\xAB" + "\xAC" + "\xAD" + "\xAE" + "\xAF"

#print "\xB0" + "\xB1" + "\xB2" + "\xB3" + "\xB4" + "\xB5" + "\xB6" + "\xB7"
#print "\xB8" + "\xB9" + "\xBA" + "\xBB" + "\xBC" + "\xBD" + "\xBE" + "\xBF"

#print "\xC0" + "\xC1" + "\xC2" + "\xC3" + "\xC4" + "\xC5" + "\xC6" + "\xC7"
#print "\xC8" + "\xC9" + "\xCA" + "\xCB" + "\xCC" + "\xCD" + "\xCE" + "\xCF"

#print "\xD0" + "\xD1" + "\xD2" + "\xD3" + "\xD4" + "\xD5" + "\xD6" + "\xD7"
#print "\xD8" + "\xD9" + "\xDA" + "\xDB" + "\xDC" + "\xDD" + "\xDE" + "\xDF"

#print "\xE0" + "\xE1" + "\xE2" + "\xE3" + "\xE4" + "\xE5" + "\xE6" + "\xE7"
#print "\xE8" + "\xE9" + "\xEA" + "\xEB" + "\xEC" + "\xED" + "\xEE" + "\xEF"

#print "\xF0" + "\xF1" + "\xF2" + "\xF3" + "\xF4" + "\xF5" + "\xF6" + "\xF7"
#print "\xF8" + "\xF9" + "\xFA" + "\xFB" + "\xFC" + "\xFD" + "\xFE" + "\xFF"