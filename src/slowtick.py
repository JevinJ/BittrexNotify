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


# This is used to delete files from a previous run, called in
# Application __init__ or used to remove out of date files
def delete_ancient_pickles(max_range=0):
    max_range = abs(max_range)
    files = glob.glob('slow_history/*pickle')
    files.sort(key=os.path.getmtime)
    for i in range(len(files)-max_range):
        os.remove(files[i])


def save_pickle(latest_data):
    date_time = time.strftime('%H%M', time.localtime())
    with open('slow_history/' + date_time + '.pickle', 'wb') as f:
        pickle.dump(latest_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    delete_ancient_pickles(LOOKBACK)


# Getting filenames for last(LOOKBACK) pickle files and
#   removing files that are out of date.
def open_pickles():
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
    prev_data = dict(open_pickles())
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