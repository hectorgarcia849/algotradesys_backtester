from zipline.api import order_target, order_target_percent, record, symbol, set_benchmark
import zipline
import matplotlib.pyplot as plt
import trading_calendars
from financial_data.APIs.api import AlphaVantageAPI
from analysis.backtest.abstract_classes import AbstractBackTester


class MovingAverageStrategy(AbstractBackTester):

    _portfolio = None

    def __init__(self):
        super().__init__()

    @classmethod
    def initialize(cls, context):
        context.i = 0
        context.asset = symbol('MSFT')
        context.assets = [symbol(asset) for asset in cls._portfolio.assets]
        set_benchmark(symbol('benchmark'))

    @classmethod
    def before_trading_start(cls):
        pass

    @classmethod
    def handle_data(cls, context, data):

        context.i += 1

        if context.i < 300:
            return

        short_mavg = data.history(context.asset, 'price', bar_count=100, frequency="1d").mean()
        long_mavg = data.history(context.asset, 'price', bar_count=300, frequency="1d").mean()

        # Trading logic

        print('cash: ', context.portfolio.cash)
        if short_mavg > long_mavg and context.portfolio.cash > 0:
            # order_target_percent orders as many shares as needed to
            # achieve the desired number of shares as percentage of the models
            order_target_percent(context.asset, .10)
        elif short_mavg < long_mavg:
            order_target(context.asset, 0)

        record(asset_prices=data.current(context.asset, 'price'),
               short_mavg=short_mavg,
               long_mavg=long_mavg)

        # note you could save prices of all stocks without explicitly typing them by putting them in dict objs, call variable prices
        # record(TSX_MSI=data.current(symbol('TSX:MSI'), 'price'))

        record(cash=context.portfolio.cash)

    @classmethod
    def analyze(cls, context, performance):
        print('_portfolio : ', cls._portfolio)
        print('context : ', context.assets)
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        performance.portfolio_value.plot(ax=ax1)
        ax1.set_ylabel('models value in $')

        ax2 = fig.add_subplot(212)
        performance['asset_prices'].plot(ax=ax2)
        performance[['short_mavg', 'long_mavg']].plot(ax=ax2)

        perf_trans = performance.ix[[t != [] for t in performance.transactions]]
        buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
        sells = perf_trans.ix[
            [t[0]['amount'] < 0 for t in perf_trans.transactions]]
        ax2.plot(buys.index, performance.short_mavg.ix[buys.index],
                 '^', markersize=10, color='m')
        ax2.plot(sells.index, performance.short_mavg.ix[sells.index],
                 'v', markersize=10, color='k')
        ax2.set_ylabel('price in $')
        plt.legend(loc=0)
        plt.show()

    def run(self, portfolio, start, end, capital_base=100000):
        MovingAverageStrategy._portfolio = portfolio
        data, _ = AlphaVantageAPI.get_daily_data_for(portfolio.assets)
        data['benchmark'] = data[portfolio.benchmark]
        assets_panel = MovingAverageStrategy.to_panel(data)
        nyse_calendar = trading_calendars.get_calendar('XNYS')

        portfolio.performance = zipline.run_algorithm(start=start,
                                                      end=end,
                                                      data_frequency='daily',
                                                      capital_base=capital_base,
                                                      before_trading_start=MovingAverageStrategy.before_trading_start(),
                                                      initialize=MovingAverageStrategy.initialize,
                                                      handle_data=MovingAverageStrategy.handle_data,
                                                      analyze=MovingAverageStrategy.analyze,
                                                      trading_calendar=nyse_calendar,
                                                      data=assets_panel)
