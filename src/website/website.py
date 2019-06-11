import requests

class Website:
    def __init__(self, api_address):
        self._api_address = api_address

    def get(self):
        response = requests.get(self.api_address)
        if response.status_code != 200:
            raise ConnectionError(f'Failed to connect with api, status code: {response.status_code}')
        return response

    @property
    def api_address(self):
        return self._api_address



