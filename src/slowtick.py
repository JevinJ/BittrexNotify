import certifi
import glob
import json
import os
import pickle
import time
import urllib3


LOOKBACK = -1
MIN_PRICE = 0.00001000
MIN_CHANGE = 3
MIN_VOL = 350


# This will be called in __init__ for Application class, it will
#  delete all old pickle files so we start with a clean dataset.
def delete_pickles():
    files = glob.glob('slow_history/*pickle')
    for file in files:
        os.remove(file)


def save_pickle(latest_data):
    date_time = time.strftime('%H%M', time.localtime())
    with open('slow_history/' + date_time + '.pickle', 'wb') as f:
        pickle.dump(latest_data, f, protocol=pickle.HIGHEST_PROTOCOL)


# Getting filenames for last(LOOKBACK) pickle files.
def open_pickle():
    files = glob.glob('slow_history/*pickle')
    if not files:
        return []
    files.sort(key=os.path.getmtime)
    with open(files[LOOKBACK], 'rb') as f:
        return pickle.load(f)


def heartbeat():
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    page = http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data
    data = json.loads(page)

    # Processing for saving latest data from Bittrex API
    latest_data = {}
    for i in data['result']:
        name = i['Market']['MarketCurrencyLong']
        last_price = i['Summary']['Last']
        last_vol = i['Summary']['BaseVolume']
        if i['Market']['BaseCurrency'] == 'BTC' and last_price >= MIN_PRICE and last_vol >= MIN_VOL:
            latest_data[name] = {'Market': i['Market'], 'Summary': i['Summary']}

    # Processing change between prev data and new, returning
    #  change for output in GUI
    prev_data = dict(open_pickle())
    ticker_data = []
    if prev_data:
        for name in latest_data:
            volume = latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0)
            old_price = latest_data.get(name, {}).get('Summary', {}).get('Last', 0)
            new_price = prev_data.get(name, {}).get('Summary', {}).get('Last', 0)
            if old_price != 0 and new_price != 0:
                change = (((new_price - old_price) / old_price) * 100)
                if change >= MIN_CHANGE:
                    ticker_data.append([name,
                                        float('{:.02f}'.format(change)),
                                        float('{:.02f}'.format(volume))])

    save_pickle(latest_data)
    return ticker_data
