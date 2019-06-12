from .website import Website


class Poloniex(Website):
    def __init__(self):
        super().__init__(website_name='poloniex')

    @property
    def markets_summary(self):
        summary = super().markets_summary
        return summary