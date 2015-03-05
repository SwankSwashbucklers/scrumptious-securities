import urllib.parse       # Stock
import urllib.request     #
import urllib.error       #
import re                 # Scraper_Stock
import json               # YQL_Stock
import os                 # TickerStock

class Stock(object):
    def __init__(self, url, **data):
        super(Stock, self).__init__()
        self.endpoint = url + '?' + urllib.parse.urlencode(data)


    def make_request(self): #TODO: log rather than print
        try:
            return urllib.request.urlopen(self.endpoint)
        except urllib.error.URLError as e:
            print("URLError = ", str(e.reason))
        except urllib.error.HTTPError as e:
            print("HTTPError = ", str(e.code))
        except Exception:
            print("Unknown exception")
        return None



class Scraper_Stock(Stock):
    def __init__(self, ticker):
        self.data = {}
        self.data['Name']  = ""
        self.data['Value'] = 0.0
        
        super(Scraper_Stock, self).__init__(
            "http://finance.yahoo.com/q", s = ticker.lower())
        self.refresh_data()


    def refresh_data(self):
        resp = super(Scraper_Stock, self).make_request()
        if not resp is None:
            response = str(resp.read())
            
            re_value = re.compile(r'<\s?span[^>]*class="[^"]*time_rtq_ticker[^"]*"[^>]*><\s?span[^>]*>([0-9.]*)')
            match = re_value.search(response)
            if not match is None: # log that regex didnt match when you get around to logging
                self.data['Value'] = float(match.group(1).strip())

            if not (self.data['Name']):
                re_name = re.compile(r'<\s?div[^>]*class="[^"]*title[^"]*"[^>]*><\s?h2[^>]*>([^<]*)')
                match = re_name.search(response)
                if not match is None: # log that regex didnt match when you get around to logging
                    self.data['Name'] = match.group(1).strip()



class YQL_Stock(Stock):
    def __init__(self, ticker, *fields):
        self.data = {}
        for f in range(0, len(fields)):
            self.data[fields[f]] = None
        sql_stmt     = "SELECT %s FROM %s WHERE symbol=\"%s\""
        field_string = ", ".join(fields)
        table        = "yahoo.finance.quotes"

        super(YQL_Stock, self).__init__(
            "https://query.yahooapis.com/v1/public/yql",
            q           = sql_stmt % (field_string, table, ticker),
            format      = "json",
            diagnostics = "false",
            env         = "store://datatables.org/alltableswithkeys",
            callback    = "" )
        self.refresh_data()


    def refresh_data(self):
        resp = super(YQL_Stock, self).make_request()
        if not resp is None: 
            response = json.loads(resp.read().decode("utf8"))
            for key in self.data:
                self.data[key] = response['query']['results']['quote'][key]



class TickerStock(object):
    def __init__(self, ticker):
        self.ticker = ticker
        self.scraper = Scraper_Stock(ticker)
        self.yql     = YQL_Stock(ticker, 'PreviousClose', 'Open')


    def get_name_string(self):
        return self.ticker if not (self.scraper.data['Name']) else self.scraper.data['Name']


    def get_value_string(self):
        value   = self.scraper.data['Value']
        p_close = float(self.yql.data['PreviousClose'])
        if (value):
            if (p_close):
                if (value > p_close):
                    dir_string = "\x1E " if os.name == 'nt' else "▲ " 
                elif (value < p_close):
                    dir_string = "\x1F" if os.name == 'nt' else "▼"
                else:
                    dir_string = "\x3D " if os.name == 'nt' else "■ "
                percent = ((value - p_close)/p_close)*100
                percent_string = '%.3f' % percent
            else:
                dir_string = "\x16" if os.name == 'nt' else "▬"
                percent_string = "--.---"
            value_string = '%.2f' % value
            space = " "
            for x in range(0, 7-len(value_string)):
                    space += " "
            return "" + value_string + space + dir_string + " " + percent_string + " %"
        return "" + "N/A"