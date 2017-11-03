import certifi
import glob
import json
import os
import pickle
import time
import urllib3


# This will be called in __init__ for GUIslowmarket class, it will
#  delete all old pickle files so we start with a clean dataset.
def delete_ancient_pickles(max_range=0):
    max_range = abs(max_range)
    files = glob.glob('slow_history/*pickle')
    files.sort(key=os.path.getmtime)
    for i in range(len(files)-max_range):
        os.remove(files[i])


def save_pickle(latest_data, cfg):
    date_time = time.strftime('%H%M', time.localtime())
    with open('slow_history/' + date_time + '.pickle', 'wb') as f:
        pickle.dump(latest_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    delete_ancient_pickles(cfg.SLOWTICK_LB)


# Getting filenames for last(LOOKBACK) pickle files and
#   removing files that are out of date.
def open_pickles(cfg):
    files = glob.glob('slow_history/*pickle')
    if not files:
        return []
    files.sort(key=os.path.getmtime)
    with open(files[cfg.SLOWTICK_LB], 'rb') as f:
        return pickle.load(f)


def heartbeat(cfg):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    page = http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data
    data = json.loads(page)

    # Processing for saving latest data from Bittrex API
    latest_data = {}
    for i in data['result']:
        name = i['Market']['MarketCurrencyLong']
        last_price = i['Summary']['Last']
        last_vol = i['Summary']['BaseVolume']
        if i['Market']['BaseCurrency'] == 'BTC' and last_price >=\
                cfg.SLOWTICK_MIN_PRICE and last_vol >= cfg.SLOWTICK_MIN_VOL:
                    latest_data[name] = {'Market': i['Market'], 'Summary': i['Summary']}

    # Processing change between prev data and new, returning
    #  change for output in GUI
    prev_data = dict(open_pickles(cfg))
    ticker_data = []
    if prev_data:
        for name in latest_data:
            volume = latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0)
            old_price = latest_data.get(name, {}).get('Summary', {}).get('Last', 0)
            new_price = prev_data.get(name, {}).get('Summary', {}).get('Last', 0)
            if old_price != 0 and new_price != 0:
                change = (((new_price - old_price) / old_price) * 100)
                if change >= cfg.SLOWTICK_MIN_CHANGE:
                    ticker_data.append([name,
                                        float('{:.02f}'.format(change)),
                                        float('{:.02f}'.format(volume))])

    save_pickle(latest_data, cfg)
    return ticker_data