import sys
import os
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from financial_data.APIs.api import AlphaVantageAPI
# from datetime import datetime
# import pytz
# import scipy.optimize as optimization
from analysis.backtest.strategies.modern_portfolio_theory.markowitz import MarkowitzModel
from analysis.backtest.strategies.modern_portfolio_theory.capm import CAPM

from models.portfolio import Portfolio

if __name__ == "__main__":
    sys.path.append(os.getcwd() + '\\')

    #  markowitz model

    # start = datetime(2010, 1, 1, 0, 0, 0, 0, pytz.utc)
    # end = datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)

    benchmark = '^GSPC'
    stocks = ['AAPL', 'MSFT', 'WMT', 'AMZN']

    p = Portfolio(stocks, benchmark)
    p.download_historical_data()
    print(p.historical_data)
    m = MarkowitzModel(p)
    m.generate_portfolios()
    m.plot_portfolios()
    m.find_optimal_weights()
    print(m.optimal_weights)
    p.weights = m.optimal_weights
    m.print_optimal_portfolio()
    m.plot_optimal_portfolio()

    # CAPM
    capm = CAPM(p)
    capm.run()
    capm.plot()
    print(capm.results)


