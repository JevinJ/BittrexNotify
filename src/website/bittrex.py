from .website import Website

class Bittrex(Website):
    def __init__(self):
        super().__init__(api_address='https://api.bittrex.com/v3/markets/summaries')

