# Value at Risk measures the probability distribution
# main assumption is that daily returns have a normal distribution (approx)
# allows to define return as a random variable drawn from a normal distribution
# to define normal distribution require: mean and standard deviation

# Value at risk is a number measure in price units.  Using a probabilility distribution it can estimate
# percentage of how likely it is to lose X amount.
# VaR measures the amount of potential loss that could happen in an investment (or a portfolio of investments)
# over a given period of time (with a given degree of confidence).

# VaR is very easy to understand / interpret
# VaR allows you to compare different types of assets or portfolios with VaR.  You can compare profitability and risk of
# different units and make a decision accordingly 'risk budgeting'

# Variance method: assumes returns are normally distributed
# i.e. on feb 10, 2017, we own 100 shares of AAPL.  The max loss tomorrow is $1750 with 99% confidence level.
# VaR is $1750
# the density normal distribution function is important:

# f(x) = (1 / sqrt(2*PI*sd^2))e^-((x-mu)^2/2sd^2)

# the integral of the function yields the probability, the definite integral is the area under the bell-shaped curve

# We would liket o mae sure that the loss is not going to be greater than some pre-defined value:
# { sigma*mu <= -$5 mil } = 0.05 (if the confidence level is 95%)
# generally {sigma*mu <= -VaR } = 1 - c

# note in order to find VaR for a greater period of time, if working with daily returns:
# sigma(n-day) = sigma(daily)*sqrt(n)
# mu(n-day) = mu(daily)*n

import numpy as np
from scipy.stats import norm


class VaR:

    def __init__(self, portfolio, confidence_level=0.99):
        super(self)
        self._confidence_level = confidence_level
        self._returns = VaR._prepare_data(portfolio)

    @property
    def confidence_level(self):
        return self.confidence_level

    @confidence_level.setter
    def confidence_level(self, confidence_level):
        if 0 <= confidence_level <= 100:
            self._confidence_level = confidence_level
        else:
            raise ValueError('Confidence level should be between 0 and 1.0')

    @staticmethod
    def _prepare_data(portfolio):
        d = {}
        for asset in portfolio.historical_data.keys():
            returns = portfolio.historical_data[asset].pct_change()
            d[asset] = {
                'returns': returns * portfolio.weights[asset],
                'mean': np.mean(returns),
                'std': np.std(returns)
            }

        return d

    # VaR for n days
    def run(self, position, mu, sigma, days=14):
        # position
        alpha = norm.ppf(1-self.confidence_level)
        var = position*(mu*days-sigma*alpha*np.sqrt(days))
        return var
