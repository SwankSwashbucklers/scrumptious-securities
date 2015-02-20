from stock import TickerStock
import math, time, os
import sys, signal

MAX_LENGTH   = 80
H_BUFFER     = 2
V_BUFFER     = 4
REFRESH_RATE = 5
WATCHLIST    = ['TSLA', 'GOOGL', 'GOOG', 'AAPL', 'OMCL', 'AAL', 'LUV', 'GPRO', 'ERII', 
				'AMZN', 'NFLX', 'MA', 'GM', 'F', 'HMC', 'HEMP', 'PHOT']


def signal_handler(signal, frame):
        print "\nScript terminated by user"
        sys.exit(0)

os.system('cls' if os.name == 'nt' else 'clear')
signal.signal(signal.SIGINT, signal_handler)


stocks = []
for ticker in WATCHLIST:
	stocks.append(TickerStock(ticker))


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

	os.system('cls' if os.name == 'nt' else 'clear')
	for l in range(0, len(output)):
		if (l % 3 == 0) and not (l == 0):
			for x in range(0, V_BUFFER):
				print ""
		print output[l]
	time.sleep(REFRESH_RATE)