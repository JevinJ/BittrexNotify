import json
import pickle
import glob
import time
from decimal import *
from bs4 import BeautifulSoup as bs
import urllib3

http = urllib3.PoolManager()
page = bs(http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data)
data = json.loads(str(page))

#todo: change this, ambiguous
def print_prices(prices_list):
	prices_list = sorted(prices_list, key=lambda t: t[1], reverse=True)
	max_len = len(max(prices_list, key=lambda x:len(x[0]))[0])
	for i in prices_list:
		print(i[0] + (' ' * ((max_len+1)-len(i[0]))) + str(i[1]))
		
def save_pickle(prices_dict):
	date_time = time.strftime('%H%M', time.localtime())
	with open('price_pickles/'+date_time+'.pickle', 'wb') as f:
		pickle.dump(prices_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
		
def open_pickle():
	glob_files = glob.glob('price_pickles/*pickle')
	for file_name in glob_files:
		print(file_name)
		with open(file_name, 'rb') as f:
			yield pickle.load(f)
	
prices_dict = {}
prices_list = []
for i in data['result']:
	if i['Market']['BaseCurrency'] == 'BTC':
		name = i['Market']['MarketCurrencyLong']
		last = i['Summary']['Last']
		prev_day = i['Summary']['PrevDay']
		perc_change = (((last-prev_day)/prev_day)*100)
		prices_dict[name] = float('{:.02f}'.format(perc_change))
		prices_list.append((name, float('{:.02f}'.format(perc_change))))

#print_prices(prices_list)

#todo: compare file names to sort by latest
last_dicts = list(open_pickle())
save_pickle(prices_dict)



	
	