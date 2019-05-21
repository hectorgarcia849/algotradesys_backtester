import numpy as np
import matplotlib.pyplot as plt


def calculate_return_rate(closing_price):
    return np.log(closing_price / closing_price.shift(1))


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
