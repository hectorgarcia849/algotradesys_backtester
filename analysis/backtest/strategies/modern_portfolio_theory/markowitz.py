from models.portfolio import Portfolio
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import analysis.backtest.strategies.modern_portfolio_theory.mpt_functions as mpt
from collections import OrderedDict
import pandas as pd

# Markowitz (MPT): Formulation for risk diversification in investing, that aims to select a group of investment
# assets which collectively have lower risk than any single asset on its own.  The objective is to choose a portfolio
#  with the maximum possible expected return for a given amount of risk.


class MarkowitzModel:

    def __init__(self, portfolio):
        self._portfolio = portfolio
        self._weights = self.initialize_weights()
        self._optimum = None
        self._preturns = None
        self._pvolatilities = None
        self._data = None

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self, portfolio):
        if isinstance(portfolio, Portfolio):
            self._portfolio = portfolio
        else:
            raise TypeError('instance variable portfolio must be of type Portfolio')

    @property
    def weights(self):
        return self._weights

    @property
    def daily_returns_of_assets(self):
        return mpt.calculate_return_rate(self._data)

    @property
    def optimal_weights(self):
        opt_port = OrderedDict()
        for asset_name, weight in zip(self.daily_returns_of_assets.columns, self._optimum['x'].round(3)):
            opt_port[asset_name] = weight
        return opt_port

    def _prepare_data(self):
        data = pd.DataFrame([self.portfolio.historical_data[k]['adj. close'] for k in self.portfolio.historical_data.keys()]).transpose()
        data.columns = self.portfolio.asset_tickers
        self._data = data.drop([self.portfolio.benchmark], axis=1)

    def initialize_weights(self):
        weights = np.random.random(self.portfolio.n_assets)
        weights /= np.sum(weights)
        return weights

    def generate_portfolios(self):
        # Monte-Carlo Simulation
        self._prepare_data()
        preturns = np.array([])
        pvolatilaties = np.array([])

        for i in range(10000):
            weights = self.initialize_weights()
            preturns = np.append(preturns,
                                 mpt.calculate_yearly_portfolio_return(self.daily_returns_of_assets, weights))
            pvolatilaties = np.append(pvolatilaties,
                                     mpt.calculate_yearly_portfolio_volatility(self.daily_returns_of_assets, weights))
        self._preturns = preturns
        self._pvolatilities = pvolatilaties

    def plot_portfolios(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self._pvolatilities,
                    self._preturns,
                    c=mpt.calculate_ex_ante_sharpe_ratio(self._preturns, self._pvolatilities),
                    marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        plt.show()

    @staticmethod
    def statistics(daily_returns_of_assets, weights):
        preturn = mpt.calculate_yearly_portfolio_return(daily_returns_of_assets, weights)
        pvol = mpt.calculate_yearly_portfolio_volatility(daily_returns_of_assets, weights)
        sharpe = mpt.calculate_ex_ante_sharpe_ratio(preturn, pvol)
        return np.array([preturn, pvol, sharpe])

    @staticmethod
    def min_func_sharpe(weights, daily_returns_of_assets):
        preturn = mpt.calculate_yearly_portfolio_return(daily_returns_of_assets, weights)
        pvol = mpt.calculate_yearly_portfolio_volatility(daily_returns_of_assets, weights)
        sharpe = mpt.calculate_ex_ante_sharpe_ratio(preturn, pvol)
        return -sharpe

    def find_optimal_weights(self):

        if len(self._data) > 0:

            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # sum of weights is 1
            bounds = tuple((0, 1) for x in range(len(self.weights)))  # max weights value is 1, min is 0
            self._optimum = optimization.minimize(fun=MarkowitzModel.min_func_sharpe,
                                                  x0=self.weights,
                                                  args=self.daily_returns_of_assets,
                                                  method='SLSQP',
                                                  bounds=bounds,
                                                  constraints=constraints)
            return self._optimum
        raise ValueError('Please run download_data method prior to optimize_portfolio method')

    def print_optimal_portfolio(self):
        opt_weights = self._optimum['x'].round(3)

        print('Optimal Portfolio Weights: ', self.optimal_weights)
        print('Expected return, volatility and sharpe ratio: ',
              self.statistics(self.daily_returns_of_assets, opt_weights))

    def plot_optimal_portfolio(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self._pvolatilities, self._preturns, c=self._preturns / self._pvolatilities, marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        opt_weights = self._optimum['x']
        plt.plot(MarkowitzModel.statistics(self.daily_returns_of_assets, opt_weights)[1],
                 MarkowitzModel.statistics(self.daily_returns_of_assets, opt_weights)[0],
                 'g*',
                 markersize=20.0)
        plt.show()
