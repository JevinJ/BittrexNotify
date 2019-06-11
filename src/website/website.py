import requests

class Website:
    def __init__(self, api_address):
        self._api_address = api_address

    def get(self):
        response = requests.get(self.api_address)
        response.raise_for_status()
        return response

    @property
    def api_address(self):
        return self._api_address



