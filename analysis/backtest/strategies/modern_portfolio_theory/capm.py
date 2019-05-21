import matplotlib.pyplot as plt
import analysis.backtest.strategies.modern_portfolio_theory.mpt_functions as mpt
import numpy as np
import pandas as pd


class CAPM:

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self._data = None
        self._monthly_returns_of_assets = None
        self.results = None
        self._portfolio_monthly_returns = None
        self._benchmark_monthly_returns = None

    def _prepare_data(self):
        tickers = list(set(self.portfolio.assets + [self.portfolio.benchmark]))
        data = pd.DataFrame([self.portfolio.historical_data[k]['adj. close'] for k in
                             self.portfolio.historical_data.keys()]).transpose()
        data.columns = tickers
        self._data = data.drop([self.portfolio.benchmark], axis=1)
        self._data = data.resample('M').last().dropna()

    def run(self, risk_free=0.05):
        self._prepare_data()
        self._monthly_returns_of_assets = mpt.calculate_return_rate(self._data)

        cov_matrix = self._monthly_returns_of_assets.cov()
        print(cov_matrix)
        print('tickers: ', self.portfolio.assets, 'weights: ', self.portfolio.weights)
        portfolio_beta_f = 0

        for ticker in self.portfolio.assets:
            b = cov_matrix.loc[ticker, self.portfolio.benchmark] / cov_matrix.loc[self.portfolio.benchmark, self.portfolio.benchmark]
            print('ticker: ', ticker)
            w = self.portfolio.weights[ticker]
            portfolio_beta_f += (b*w)

        print("Beta from forumula: ", portfolio_beta_f)
        print('weights: ', list(self.portfolio.weights.values()))

        weighted_portfolio_assets = self._monthly_returns_of_assets.drop([self.portfolio.benchmark], axis=1).dropna() * list(self.portfolio.weights.values())
        self._portfolio_monthly_returns = np.sum(weighted_portfolio_assets, axis=1)
        self._benchmark_monthly_returns = self._monthly_returns_of_assets[self.portfolio.benchmark].dropna()

        print('Y', self._portfolio_monthly_returns.head(), 'len: ', len(self._portfolio_monthly_returns.index))
        print('x', self._benchmark_monthly_returns.head(), 'len: ', len(self._benchmark_monthly_returns.index))

        portfolio_beta_r, portfolio_alpha = np.polyfit(self._benchmark_monthly_returns, self._portfolio_monthly_returns, deg=1)
        print("Beta from Regression: ", portfolio_beta_r)

        self.results = {
            'Expected Yr Returns': risk_free + portfolio_beta_r * (self._monthly_returns_of_assets[self.portfolio.benchmark].mean() * 12 - risk_free),
            'portfolio_alpha': portfolio_alpha,
            'portfolio_beta_f': portfolio_beta_f,
            'portfolio_beta_r': portfolio_beta_r
        }

        print('Results: ', self.results)

    def plot(self):
        fig, axis = plt.subplots(1, figsize=(20, 10))
        axis.scatter(self._benchmark_monthly_returns, self._portfolio_monthly_returns, label="Data points")
        axis.plot(self._benchmark_monthly_returns, self.results['portfolio_beta_r'] * self._benchmark_monthly_returns + self.results['portfolio_alpha'], color='red', label="CAPM Line")
        plt.title("Capital Asset Pricing Model, finding alpha and betas")
        plt.xlabel("Market return $R_m$", fontsize=10)
        plt.ylabel("Portfolio return $R_a$: {}".format(self.portfolio.assets))
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()

