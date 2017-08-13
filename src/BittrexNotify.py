import json
from decimal import *
from bs4 import BeautifulSoup as bs
import urllib3

http = urllib3.PoolManager()
page = bs(http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data)
data = json.loads(str(page))

for i in data['result']:
	if i['Market']['BaseCurrency'] == 'BTC':
		name = i['Market']['MarketCurrencyLong']
		last = i['Summary']['Last']
		prev_day = i['Summary']['PrevDay']
		perc_change = (((last-prev_day)/prev_day)*100)
		print(name + (' ' * (30-len(name))) + '{:.02f}'.format(perc_change) + '%')
	

	