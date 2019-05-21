import sys
import os
from analysis.backtest.strategies.technical_analysis.moving_average import MovingAverageStrategy
from datetime import datetime
import pytz
from models.portfolio import Portfolio

if __name__ == "__main__":
    sys.path.append(os.getcwd() + '\\')
    start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2019, 1, 1, 0, 0, 0, 0, pytz.utc)
    assets = ['MSFT', 'TSX:MSI']
    benchmark = 'MSFT'
    portfolio = Portfolio(assets, benchmark)
    mov_avg_strategy = MovingAverageStrategy()
    mov_avg_strategy.run(portfolio, start, end)

    print(portfolio.performance)
    print(portfolio.performance[['portfolio_value', 'benchmark_period_return']])
