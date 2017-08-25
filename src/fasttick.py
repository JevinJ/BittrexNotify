import json
import pickle
import os
import glob
import time
import urllib3
import certifi


def delete_pickle():
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
    for file in files[-9:]:
        with open(file, 'rb') as f:
            yield pickle.load(f)

def heartbeat():
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    page = http.request('GET', 'https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries').data
    data = json.loads(page)

    latest_data = {}
    ticker_data = []
    for i in data['result']:
        name = i['Market']['MarketCurrencyLong']
        last_price = i['Summary']['Last']
        yday_price = i['Summary']['PrevDay']
        last_vol = i['Summary']['BaseVolume']
        if i['Market']['BaseCurrency'] == 'BTC' and last_price >= 0.00001000 and last_vol >= 350:
            change = (((last_price - yday_price) / yday_price) * 100)
            latest_data[name] = {'Market': i['Market'], 'Summary': i['Summary']}
            ticker_data.append((name, '{:.02f}'.format(change)))

    prev_data = list(open_pickle())
    prev_data.append(latest_data)
    ticker_data = []
    if prev_data:
        for name in latest_data:
            prev_changes = []
            for i in range(len(prev_data) - 1):
                old = prev_data[i].get(name, {}).get('Summary', {}).get('Last', 0)
                new = prev_data[i + 1].get(name, {}).get('Summary', {}).get('Last', 0)
                if old != 0 and new != 0:
                    prev_changes.append((((new - old) / old) * 100))
            if prev_changes:
                average_rate = (sum(prev_changes) / len(prev_changes))
                volume = latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0)
                if average_rate >= .3:
                    ticker_data.append([name, '+{:.02f}'.format(average_rate)+'%', '{:.02f}'.format(volume)])

    save_pickle(latest_data)
    return sorted(ticker_data, key=lambda x: x[1], reverse=True)
