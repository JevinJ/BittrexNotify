import json
import pickle
import os
import glob
import time
from decimal import *
from bs4 import BeautifulSoup as bs
import urllib3

http = urllib3.PoolManager()
page = bs(http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data)
data = json.loads(str(page))


def print_ticker(latest_data_list):
	if not latest_data_list:
		return
	latest_data_list.sort(key=lambda x: x[1], reverse=True)
	max_len = len(max(latest_data_list, key=lambda x:len(x[0]))[0])
	for i in latest_data_list:
		print(i[0] + (' ' * ((max_len+1)-len(i[0]))) + i[1])
		
def save_pickle(prices_dict):
	date_time = time.strftime('%H%M', time.localtime())
	with open('history/'+date_time+'.pickle', 'wb') as f:
		pickle.dump(prices_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
		
def open_pickle():
	glob_files = glob.glob('history/*pickle')
	if not glob_files:
		return []
	glob_files.sort(key=os.path.getmtime, reverse=True)
	with open(glob_files[0], 'rb') as f:
		print(glob_files[0])
		return pickle.load(f)

	
while(True):
	latest_data = {}
	latest_data_list = []
	for i in data['result']:
		name = i['Market']['MarketCurrencyLong']
		last_price = i['Summary']['Last']
		yday_price = i['Summary']['PrevDay']
		last_vol = i['Summary']['BaseVolume']
		if i['Market']['BaseCurrency'] == 'BTC' and last_vol >= 350:
			change = (((last_price-yday_price)/yday_price)*100)
			latest_data[name] = i
			latest_data_list.append([name, '{:.02f}'.format(change)])
	#print_ticker(latest_data_list)
	
	
	prev_data = dict(open_pickle())
	to_notify = []
	if prev_data:
		for name in latest_data:
			last_price = latest_data[name]['Summary']['Last']
			prev_data_price = prev_data[name]['Summary']['Last']
			if (last_price - prev_data_price) > 3:
				print_ticker([name, '+'+'{:.02f}'.format(last_price - prev_data_price)])
				to_notify.append((name, float('{:.02f}'.format(last_price))))
				
	
	save_pickle(latest_data)
	
	print("SLEEPING")
	time.sleep(350)
