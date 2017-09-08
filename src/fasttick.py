import certifi
import glob
import json
import os
import pickle
import time
import urllib3


LOOKBACK = -9
MIN_RATE = .2
MIN_VOL = 350


def delete_pickles():
    files = glob.glob('fast_history/*pickle')
    for file in files:
        os.remove(file)


def save_pickle(latest_data):
    date_time = time.strftime('%M%S', time.localtime())
    with open('fast_history/' + date_time + '.pickle', 'wb') as f:
        pickle.dump(latest_data, f, protocol=pickle.HIGHEST_PROTOCOL)


def open_pickle():
    files = glob.glob('fast_history/*pickle')
    if not files:
        return []
    files.sort(key=os.path.getmtime)
    for file in files[LOOKBACK:]:
        with open(file, 'rb') as f:
            yield pickle.load(f)


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
        if i['Market']['BaseCurrency'] == 'BTC' and last_price >= 0.00001000 and last_vol >= MIN_VOL:
            latest_data[name] = {'Market': i['Market'], 'Summary': i['Summary']}

    # Processing all data within 9 ticks + latest and returning
    #  rate for output in GUI
    prev_data = list(open_pickle())
    prev_data.append(latest_data)
    ticker_data = []
    if prev_data:
        for name in latest_data:
            prev_changes = []
            for i in range(len(prev_data)-1):
                old_price = prev_data[i].get(name, {}).get('Summary', {}).get('Last', 0)
                new_price = prev_data[i+1].get(name, {}).get('Summary', {}).get('Last', 0)
                if old_price != 0 and new_price != 0:
                    prev_changes.append(((new_price - old_price) / old_price) * 100)
            if prev_changes:
                volume = latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0)
                average_rate = (sum(prev_changes) / len(prev_changes))
                if average_rate >= MIN_RATE:
                    ticker_data.append([name,
                                        float('{:.02f}'.format(average_rate)),
                                        float('{:.02f}'.format(volume))])

    save_pickle(latest_data)
    return sorted(ticker_data, key=lambda x: x[1], reverse=True)
