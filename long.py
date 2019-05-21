import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from financial_data.APIs.api import AlphaVantageAPI
from datetime import datetime
import pytz
import scipy.optimize as optimization
from analysis.backtest.strategies.modern_portfolio_theory.markowitz import MarkowitzModel
from analysis.backtest.strategies.modern_portfolio_theory.capm import CAPM

from models.portfolio import Portfolio

def download_data(stocks):
    res, _ = AlphaVantageAPI.get_daily_data_for(stocks)
    data = pd.DataFrame([res[k]['adj. close'] for k in res.keys()]).transpose()
    data.columns = stocks
    return data


def calculate_return_rates(data):
    return np.log(data/data.shift(1))


def plot_data(data):
    data.plot(figsize=(10, 5))
    plt.show()


def plot_daily_returns(daily_returns_of_assets):
    daily_returns_of_assets.plot(figsize=(10, 15))
    plt.show()


def show_statistics(daily_returns_of_assets):
    print('---Expected Yearly Returns---')
    print(daily_returns_of_assets.mean() * 252)
    print('---Covariance Matrix (Yearly)---')
    print(daily_returns_of_assets.cov() * 252)


def initialize_weights(n):
    weights = np.random.random(n)
    weights /= np.sum(weights)
    return weights


def calculate_yearly_portfolio_return(daily_returns_of_assets, weights):
    return np.sum(daily_returns_of_assets.mean() * weights) * 252


def calculate_yearly_portfolio_volatility(daily_returns_of_assets, weights):
    # volatility: standard deviation of logarithmic returns
    return np.sqrt(np.dot(weights.T, np.dot(daily_returns_of_assets.cov() * 252, weights)))


# Sharpe Ratio measures the excess return (risk premium) per unit of standard deviation

def calculate_ex_ante_sharpe_ratio(portfolio_return_rate, volatility, risk_free=0.05):
    return (portfolio_return_rate - risk_free) / volatility


def calculate_ex_post_sharpe_ratio(portfolio_return_rate, return_of_benchmark):
    excess_daily_returns = portfolio_return_rate - return_of_benchmark
    return excess_daily_returns / np.std(excess_daily_returns)


def generate_portfolios(daily_returns_of_assets):
    # Monte-Carlo Simulation
    preturns = np.array([])
    pvolatitlies = np.array([])

    for i in range(10000):
        weights = initialize_weights(len(daily_returns_of_assets.columns))
        preturns = np.append(preturns, calculate_yearly_portfolio_return(daily_returns_of_assets, weights))
        pvolatitlies = np.append(pvolatitlies, calculate_yearly_portfolio_volatility(daily_returns_of_assets, weights))

    return preturns, pvolatitlies


def plot_portfolios(portfolio_returns, portfolio_volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_volatilities,
                portfolio_returns,
                c=calculate_ex_ante_sharpe_ratio(portfolio_returns, portfolio_volatilities),
                marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()


def statistics(daily_returns_of_assets, weights):
    preturn = calculate_yearly_portfolio_return(daily_returns_of_assets, weights)
    pvol = calculate_yearly_portfolio_volatility(daily_returns_of_assets, weights)
    sharpe = calculate_ex_ante_sharpe_ratio(preturn, pvol)
    return np.array([preturn, pvol, sharpe])


def min_func_sharpe(weights, daily_returns_of_assets):
    return -statistics(daily_returns_of_assets, weights)[2]


def optimize_portfolio(daily_returns_of_assets, weights):

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # sum of weights is 1
    bounds = tuple((0, 1) for x in range(len(weights)))  # max weights value is 1, min is 0
    return optimization.minimize(fun=min_func_sharpe,
                                 x0=weights,
                                 args=daily_returns_of_assets,
                                 method='SLSQP',
                                 bounds=bounds,
                                 constraints=constraints)


def print_optimal_portfolio(optimum, daily_returns_of_assets):
    opt_weights = optimum['x'].round(3)
    opt_port = [{asset_name: weight} for asset_name, weight in zip(daily_returns_of_assets.columns, opt_weights)]
    print('Optimal Portfolio Weights: ', opt_port)
    print('Expected return, volatility and sharpe ratio: ', statistics(daily_returns_of_assets, opt_weights))


def show_optimal_portfolio(optimum, daily_returns_of_assets, portfolio_return_rates, portfolio_volatilities):
    plt.figure(figsize=(10,6))
    plt.scatter(portfolio_volatilities, portfolio_return_rates, c=portfolio_return_rates / portfolio_volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    opt_wieghts = optimum['x']
    plt.plot(statistics(daily_returns_of_assets, opt_wieghts)[1],
             statistics(daily_returns_of_assets, opt_wieghts)[0],
             'g*',
             markersize=20.0)
    plt.show()


def plot_capm(data, market_ticker, stock_ticker, alpha, beta):
    fig, axis= plt.subplots(1, figsize=(20,10))
    axis.scatter(data[market_ticker], data[stock_ticker], label="Data points")
    axis.plot(data[market_ticker], beta*data[market_ticker] + alpha, color='red', label="CAPM Line")
    plt.title("Capital Asset Pricing Model, finding alpha and betas")
    plt.xlabel("Market return $R_m$", fontsize=10)
    plt.ylabel("Stock return $R_a$")
    plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
    plt.legend()
    plt.grid(True)
    plt.show()


def capm(stock_ticker, market_ticker, risk_free=0.05):

    av_data = download_data([stock_ticker, market_ticker])
    av_data = av_data.resample('M').last()
    av_data[[stock_ticker, market_ticker]] = calculate_return_rates(av_data[[stock_ticker, market_ticker]])
    av_data = av_data.dropna()

    cov_matrix = av_data.cov()
    print(cov_matrix)

    beta = cov_matrix.loc[stock_ticker, market_ticker] / cov_matrix.loc[market_ticker, market_ticker]
    print("Beta from forumula: ", beta)

    beta, alpha = np.polyfit(av_data[market_ticker], av_data[stock_ticker], deg=1)
    print("Beta from Regression: ", beta)

    plot_capm(av_data, market_ticker, stock_ticker, alpha, beta)

    expected_yr_return = risk_free + beta*(av_data[market_ticker].mean() * 12 - risk_free)
    print('Expected Return (Yr): ', expected_yr_return)


if __name__ == "__main__":
    sys.path.append(os.getcwd() + '\\')

    #  markowitz model


    # start = datetime(2010, 1, 1, 0, 0, 0, 0, pytz.utc)
    # end = datetime(2017, 1, 1, 0, 0, 0, 0, pytz.utc)

    benchmark = '^GSPC'
    stocks = ['AAPL', 'MSFT', 'WMT', 'AMZN']

    p = Portfolio(stocks, benchmark)
    p.download_historical_data()
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


