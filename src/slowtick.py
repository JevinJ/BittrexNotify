import config
import misc


def heartbeat():
    """
    Processes data from Bittrex into a simpler dictionary,
    calls the save function on it, deletes the oldest
    saved dictionary(if it's out of lookback range), and finally
    creates a list of the best coins to be used in tkinter listboxes.
    :return: A list containing triples of (coin name, % change, volume)
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
            config.SLOWTICK_MIN_PRICE and last_vol >= config.SLOWTICK_MIN_VOL:
                latest_data[name] = {'Summary': d['Summary']}

    # Processing change between prev data and new, returning
    #  change for output in GUI
    prev_data = list(misc.open_pickles('slowtick_history', config.SLOWTICK_LOOKBACK))
    ticker_data = []
    if prev_data:
        for name in latest_data:
            volume = float(latest_data.get(name, {}).get('Summary', {}).get('BaseVolume', 0.0))
            old_price = float(latest_data.get(name, {}).get('Summary', {}).get('Last', 0.0))
            new_price = float(prev_data[-1].get(name, {}).get('Summary', {}).get('Last', 0.0))
            if old_price != 0:
                change = (((new_price - old_price) / old_price) * 100)
                if change >= config.SLOWTICK_MIN_CHANGE:
                    ticker_data.append([name,
                                        float(f'{change:.02f}'),
                                        float(f'{volume:.02f}')])

    misc.save_pickle(latest_data, 'slowtick_history')
    misc.delete_ancient_pickles('slowtick_history', config.SLOWTICK_LOOKBACK)
    return ticker_data
