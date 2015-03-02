from stock import TickerStock
import math, time, os
import sys, signal

MAX_LENGTH   = 80
H_BUFFER     = 5
V_BUFFER     = 3
REFRESH_RATE = 10
WATCHLIST    = ['TSLA', 'AAPL', 'GOOGL', 'GOOG', 'OMCL', 'ERII', 'SCTY']
#WATCHLIST    = ['TSLA', 'GOOGL', 'GOOG', 'AAPL', 'OMCL', 'AAL', 'LUV', 'GPRO', 'ERII', 
#				'AMZN', 'NFLX', 'MA', 'GM', 'F', 'HMC', 'HEMP', 'PHOT']


def signal_handler(signal, frame):
        print("\nScript terminated by user")
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
		stock.scraper.refresh_data()
		if (longest < len(stock.get_name_string())): 
			longest = len(stock.get_name_string())
		if (longest < len(stock.get_value_string())): 
			longest = len(stock.get_value_string())

	columns = int(math.floor(MAX_LENGTH/float(longest+H_BUFFER)))
	#if ((columns*longest+(columns-1)*H_BUFFER) < MAX_LENGTH): 
	#	columns = columns + 1
	rows    = int(math.ceil(len(stocks)/float(columns)))

	for r in range(0, rows):
		for x in range(0, 2):
			output.append("")
		for c in range(0, columns):
			if (c+(r*columns) >= len(stocks)):
				break
			stock = stocks[c+(r*columns)]
			output[(0)+(r*2)] += stock.get_name_string()
			output[(1)+(r*2)] += stock.get_value_string()
			if not (c==(columns-1)):
				for x in range(0, (longest-len(stock.get_name_string()))+H_BUFFER):
					output[(0)+(r*2)] += " "
				for x in range(0, (longest-len(stock.get_value_string()))+H_BUFFER):
					output[(1)+(r*2)] += " "

	os.system('cls' if os.name == 'nt' else 'clear')
	for l in range(0, len(output)):
		if (l % 2 == 0) and not (l == 0):
			for x in range(0, V_BUFFER):
				print()
		print(output[l])
	time.sleep(REFRESH_RATE)