import pandas as pd
from collections import OrderedDict
from financial_data.APIs.api import AlphaVantageAPI


class Portfolio:

    def __init__(self, assets, benchmark):
        self._assets = assets
        self._benchmark = benchmark
        self._performance = None
        self._weights = self._initialize_weights()
        self._historical_data = None

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights):
        if isinstance(weights, OrderedDict):
            acc = 0
            for asset in weights.keys():
                if asset in self.assets:
                    acc += weights[asset]
                else:
                    raise ValueError('instance weights keys must be the same as assets')
            if round(acc, 2) == 1:
                self._weights = weights
            else:
                raise ValueError('sum of weight values must equal 1')
            return
        raise TypeError('instance weights must be a dictionary object')

    def _initialize_weights(self):
        weights = OrderedDict()
        w = 1 / self.n_assets
        for ticker in self.assets:
            weights[ticker] = w
        return weights

    @property
    def assets(self):
        return self._assets

    @assets.setter
    def assets(self, assets):
        self._assets = assets

    @property
    def n_assets(self):
        return len(self.assets)

    @property
    def benchmark(self):
        return self._benchmark

    @benchmark.setter
    def benchmark(self, benchmark):
        # need to add logic to check that benchmark is in assets
        self._benchmark = benchmark

    @property
    def performance(self):
        return self._performance

    @performance.setter
    def performance(self, performance):
        self._performance = performance

    @property
    def historical_data(self):
        return self._historical_data

    @historical_data.setter
    def historical_data(self, historical_data):
        if isinstance(historical_data, pd.DataFrame) or historical_data is None:
            self._historical_data = historical_data
        else:
            raise TypeError('instance variable historical_data must be of type Pandas.DataFrame')

    def download_historical_data(self):
        tickers = list(set(self.assets + [self.benchmark]))
        res, _ = AlphaVantageAPI.get_daily_data_for(tickers)
        data = pd.DataFrame([res[k]['adj. close'] for k in res.keys()]).transpose()
        data.columns = tickers
        self.historical_data = data
