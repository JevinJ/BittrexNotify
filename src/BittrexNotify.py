import json
import pickle
import os
import sys
import glob
import time
import urllib3
import certifi


def print_ticker(data_list):
    if not data_list:
        return
    data_list.sort(key=lambda x: x[1], reverse=True)
    max_len = len(max(data_list, key=lambda x: len(x[0]))[0])
    sys.stdout.write('\a')
    for i in data_list:
        print(i[0] + (' ' * ((max_len + 1) - len(i[0]))) + i[1])

def save_pickle(latest_data):
    date_time = time.strftime('%H%M', time.localtime())
    with open('history/' + date_time + '.pickle', 'wb') as f:
        pickle.dump(latest_data, f, protocol=pickle.HIGHEST_PROTOCOL)

def open_pickle():
    glob_files = glob.glob('history/*pickle')
    if not glob_files:
        return []
    glob_files.sort(key=os.path.getmtime, reverse=True)
    with open(glob_files[0], 'rb') as f:
        return pickle.load(f)

def heartbeat():
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    page = http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data
    data = json.loads(page)

    latest_data = {}
    for i in data['result']:
        name = i['Market']['MarketCurrencyLong']
        last_price = i['Summary']['Last']
        last_vol = i['Summary']['BaseVolume']
        if i['Market']['BaseCurrency'] == 'BTC' and last_price >= 0.00001000 and last_vol >= 350:
            latest_data[name] = {'Market': i['Market'], 'Summary': i['Summary']}

    prev_data = dict(open_pickle())
    ticker_data = []
    if prev_data:
        for name in prev_data:
            volume = latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0)
            last_price = latest_data.get(name, {}).get('Summary', {}).get('Last', 0)
            prev_data_price = prev_data.get(name, {}).get('Summary', {}).get('Last', 0)
            change = (((last_price - prev_data_price) / prev_data_price) * 100)
            if change >= 3:
                ticker_data.append([name, '+{:.02f}'.format(change)+'%', '{:.02f}'.format(volume)])
    save_pickle(latest_data)
    return ticker_data



