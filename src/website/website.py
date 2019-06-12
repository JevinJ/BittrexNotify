from misc import requests_get
import yaml


class Website:
    def __init__(self, website_name):
        website_name = website_name.lower()
        with open('configs/website_configs.yaml') as website_configs:
            site_config = yaml.load(website_configs)[website_name]
            self._GET_markets_url = site_config['GET_markets_url']
            self._GET_markets_summary_url = site_config['GET_markets_summary_url']
            self._GET_market_symbol_url = site_config['GET_market_symbol_url']
            self._GET_market_symbol_summary_url = site_config['GET_market_symbol_summary_url']

    @property
    def summary(self) -> list:
        return requests_get(self._GET_markets_summary_url)



