import config
import misc


def heartbeat():
    """
    Processes data from Bittrex into a simpler dictionary,
    calls the save function on it, deletes the oldest
    saved dictionary(if it's out of lookback range), and finally
    creates a list of the best coins to be used in tkinter listboxes.
    :return: A list containing triples of (coin name, increase rate, volume)
    """
    data = misc.retrieve_data()

    # Processing for saving latest data from Bittrex API
    latest_data = {}
    for d in data.get('result', {}):
        name = d.get('Market', {}).get('MarketCurrencyLong', '')
        last_price = d.get('Summary', {}).get('Last', 0.0)
        last_vol = d.get('Summary', {}).get('BaseVolume', 0.0)
        base_currency = d.get('Market', {}).get('BaseCurrency', '')
        if base_currency == 'BTC' and last_price >= \
            config.FASTTICK_MIN_PRICE and last_vol >= config.FASTTICK_MIN_VOL:
                latest_data[name] = {'Summary': d['Summary']}

    # Processing all data within 9 ticks + latest and returning
    #  rate for output in GUI
    prev_data = list(misc.open_pickles('fasttick_history', config.FASTTICK_LOOKBACK))
    prev_data.append(latest_data)
    ticker_data = []
    if prev_data:
        for name in latest_data:
            prev_changes = []
            for i in range(len(prev_data)-1):
                old_price = float(prev_data[i].get(name, {}).get('Summary', {}).get('Last', 0.0))
                new_price = float(prev_data[i+1].get(name, {}).get('Summary', {}).get('Last', 0.0))
                if old_price != 0:
                    change = (((new_price - old_price) / old_price) * 100)
                    prev_changes.append(change)
            if prev_changes:
                volume = float(latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0.0))
                average_rate = float((sum(prev_changes) / len(prev_changes)))
                if average_rate >= config.FASTTICK_MIN_RATE:
                    ticker_data.append((name, average_rate, volume))

    misc.save_pickle(latest_data, 'fasttick_history')
    misc.delete_ancient_pickles('fasttick_history', config.FASTTICK_LOOKBACK)
    return ticker_data