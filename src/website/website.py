import requests
import yaml

class Website:
    def __init__(self, website_name):
        website_name = website_name.lower()
        with open('websites.yaml') as website_configs:
            site_config = yaml.load(website_configs)[website_name]
            self._GET_markets_url = site_config['GET_markets_url']
            self._GET_markets_summary_url = site_config['GET_markets_summary_url']
            self._GET_market_symbol_url = site_config['GET_market_symbol_url']
            self._GET_market_symbol_summary_url = site_config['GET_market_symbol_summary_url']

    @property
    def summary(self) -> list:
        return self._get_summary()

    def _get_summary(self):
        response = requests.get(self._GET_markets_summary_url)
        response.raise_for_status()
        return response.json()



