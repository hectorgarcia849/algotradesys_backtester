import requests
import json
import pandas as pd
from collections import OrderedDict


class AlphaVantageAPI:

    AV_URL = 'http://192.168.56.1:3000/services/alphavantage'

    def __init__(self):
        return

    @staticmethod
    def get_historical_daily_data(ticker_name, output_size='compact'):
        # need to update node server to correct object keys
        req = requests.get(AlphaVantageAPI.AV_URL + '/dailydata?ticker_name={}&output_size={}'
                           .format(ticker_name, output_size))
        return json.loads(req.content.decode('utf-8'))

    @staticmethod
    def get_quote(ticker_name):
        req = requests.get(AlphaVantageAPI.AV_URL + '/quote?ticker_name={}'.format(ticker_name))
        return json.loads(req.content.decode('utf-8'))

    @staticmethod
    def get_daily_data_for(assets):
        # returns pd.Panel of all assets
        asset_dict = OrderedDict()
        meta_dict = {}

        for asset in assets:
            res = AlphaVantageAPI.get_historical_daily_data(asset, output_size='full')
            df = pd.DataFrame(data=res['data'])
            df['date'] = pd.to_datetime(df['date'])
            df.index = df['date']
            df = df.drop(['date'], axis=1)
            # df = df[["open", "high", "low", "close", "volume"]]
            for col in df.columns:
                df[col] = df[col].astype('float')
            df[col] = df[col].resample("1d").mean()
            df[col].fillna(method="ffill", inplace=True)
            asset_dict[asset] = df
            meta_dict[asset] = res['meta']

        return asset_dict, meta_dict



