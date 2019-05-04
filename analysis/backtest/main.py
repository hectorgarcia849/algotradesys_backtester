from financial_data.APIs.api import AlphaVantageAPI as AV
import pandas as pd
from wip.technical_analysis.momentum import StochasticOscillatorAgent as SO

# Import data, preparation and cleaning
msi = AV.get_historical_daily_data('TSX:MSI')
msi_df = pd.DataFrame(msi['data'])
msi_df.date = pd.to_datetime(msi_df.date)
msi_df['adj. close'] = pd.to_numeric(msi_df['adj. close'])
msi_df.close = pd.to_numeric(msi_df.close)
msi_df.dividend = pd.to_numeric(msi_df.dividend)
msi_df.high = pd.to_numeric(msi_df.high)
msi_df.low = pd.to_numeric(msi_df.low)
msi_df.open = pd.to_numeric(msi_df.open)
msi_df['split coeff.'] = pd.to_numeric(msi_df['split coeff.'])
msi_df.volume = pd.to_numeric(msi_df.volume)
msi_df.drop(['symbol'], axis=1)

so = SO()
so.generate_signals(msi_df)
so.plot(msi_df)


