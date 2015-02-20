from stock import TickerStock

apple = TickerStock('AAPL')
print apple.get_name_string()
print apple.get_bid_string()
print apple.get_ask_string()