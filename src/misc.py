import glob
import pickle
import requests
import time
import os


def requests_get(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def delete_ancient_pickles(folder_name, amount_to_keep=0):
    """
    Deletes pickle files in a given folder up to a given amount of the latest files.
    :param folder_name: name of folder where pickle files are stored,
                        without slashes. eg('fasttick_history')
    :param amount_to_keep: amount of files to keep, default is to delete all.
    :return: None
    """
    if not os.path.exists(f'{folder_name}') or not os.path.lexists(f'{folder_name}'):
        raise ValueError('folder does not exist or incorrect folder name')

    files = glob.glob(f'{folder_name}/*pickle')
    files.sort(key=os.path.getmtime, reverse=True)
    for f in files[amount_to_keep:]:
        os.remove(f)


def save_pickle(latest_data, folder_name):
    """
    Saves a dictionary as a pickle file in the given folder.
    :param latest_data: a dictionary to be serialized.
    :param folder_name: name of folder where pickle files are stored,
                        without slashes. eg('fasttick_history')
    :return: None
    """
    if not os.path.exists(f'{folder_name}') or not os.path.lexists(f'{folder_name}'):
        raise ValueError('folder does not exist or incorrect folder name')

    date_time = time.strftime('%M-%S', time.localtime())
    with open(f'{folder_name}/{date_time}.pickle', 'wb') as f:
        pickle.dump(latest_data, f, protocol=pickle.HIGHEST_PROTOCOL)


def open_pickles(folder_name, lookback=0):
    """
    Yields dictionaries from pickle files in a folder.
    :param folder_name: name of folder where pickle files are stored,
                        without slashes. eg('fasttick_history')
    :param lookback: how far back from the newest file in the folder to search.
    :return: yields dictionaries
    """
    if not os.path.exists(f'{folder_name}') or not os.path.lexists(f'{folder_name}'):
        raise ValueError('folder does not exist or incorrect folder name')

    files = glob.glob(f'{folder_name}/*pickle')
    files.sort(key=os.path.getmtime)
    if not files:
        return {}
    if len(files) > lookback:
        files = [f for f in files[len(files)-lookback:]]
    for file in files:
        with open(file, 'rb') as f:
            yield pickle.load(f)
