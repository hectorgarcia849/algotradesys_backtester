from abc import ABC, abstractmethod
import pandas as pd
import pytz


class Agent(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def generate_signals(self, financial_data):
        # stock_data is a tuple of relevant stock data as Series Object
        # Returns DataFrame of Generated Signals
        pass


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
        pass

    @classmethod
    @abstractmethod
    def handle_data(cls, context, data):
        pass

    @classmethod
    @abstractmethod
    def analyze(cls, context, performance):
        pass

    @classmethod
    @abstractmethod
    def run(cls, start, end, capital_base):
        pass

    @classmethod
    def to_panel(cls, asset_dict):
        asset_panel = pd.Panel(asset_dict)
        asset_panel.minor_axis = ["open", "high", "low", "close", "volume"]
        asset_panel.major_axis = asset_panel.major_axis.tz_localize(pytz.utc)
        return asset_panel
