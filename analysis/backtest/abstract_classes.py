from abc import ABC, abstractmethod
import pandas as pd
import pytz


class AbstractBackTester(ABC):

    def __init__(self):
        super().__init__()

    @classmethod
    @abstractmethod
    def before_trading_start(cls):
        pass

    @classmethod
    @abstractmethod
    def initialize(cls, context):
        # called once before running backtest
        pass

    @classmethod
    @abstractmethod
    def handle_data(cls, context, data):
        # called every time it receives data, can be by second --> to daily.
        pass

    @classmethod
    @abstractmethod
    def analyze(cls, context, performance):
        # called once at the end of the backtest
        pass

    @classmethod
    @abstractmethod
    def run(cls, start, end, capital_base):
        pass

    @classmethod
    def to_panel(cls, asset_dict):
        for k in asset_dict.keys():
            asset_dict[k] = asset_dict[k][["open", "high", "low", "close", "volume"]]
        asset_panel = pd.Panel(asset_dict)
        asset_panel.minor_axis = ["open", "high", "low", "close", "volume"]
        asset_panel.major_axis = asset_panel.major_axis.tz_localize(pytz.utc)
        return asset_panel
