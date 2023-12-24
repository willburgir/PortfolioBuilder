"""
~~~ Ticker Loot Llama Module ~~~

⠀⠀⠀⠀⢀⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⣠⣾⣿⠇⢀⣠⣴⣤⠀⠀⠙⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⣠⣾⣿⡿⠃⠀⠀ ⠀⢀⠀⠀⠀⢀⣆⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣾⣿⣿⡿⠁⠀⠀⠀ ⠀⣾⠀⠀⠀⠀⠋⠀
  ⢠⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠠⣤⣴⣿⣷⣤⠄⠀⠀⠀
⠤⣾⡦⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀
⠀⠸⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠹⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⠟⠉⠉⠻⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢾⣿⣿⣿⣿⡟⠀⢠⣤⠀⣿⣿⣿⣿⣿⠟⢛⣋⣀⣀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⣀⠀⠙⠿⣿⣿⣷⠀⠈⠋⢀⣿⣿⣿⣿⡏⢀⣾⣿⣿⣿⡿⡄⠀⠀
⠀⠀⠀⠀⢠⣿⣷⣤⡀⠈⠻⣿⣷⣶⣾⣿⣿⣿⣿⡟⠀⣼⣿⣿⣿⣸⣧⢡⠀⠀
⠀⠀⠠⠾⣿⣿⣿⣿⣿⣦⡀⠈⠻⣿⣿⣿⣿⣿⡟⠀⣼⣿⣿⣿⣿⣿⣟⡛⠁⠀
⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣦⣄⠈⠻⣿⣿⡿⠁⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⠀⠀⠀⠘⠻⠿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣬⣭⣥⣤⡍⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣽⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠛⠛⠉⠀⠾⠿⠟⠛⠀⠿⠿⣿⡙⠛⠛⠉⠻⣿⠀⠀⠀⠀⠀⠀⠀


Use this module to obtain the input data needed for PortfolioBuilder.py

The amazing Loot Llama will help you obtain historical data on tickers and store them in Excel format. 
Works like magic, it's too easy! 

Simply change the #OPTIONS below and run the file. 

"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# OPTIONS
TICKERS   = ['BMO.TO', 'BNS.TO', 'BTCX-B.TO', 'CM.TO', 'GOOGL', 'MSFT', 'NA.TO', 'QQQ', 'RY.TO', 'TD.TO', 'VSP.TO']
YEARS     = 10
FILE_NAME = "LOOT"


# Define the list of tickers
tickers = TICKERS

# Set the end date as today
end_date = datetime.today().strftime('%Y-%m-%d')

# Calculate the start date as 10 years ago from today
start_date = (datetime.today() - timedelta(days=365 * YEARS)).strftime('%Y-%m-%d')

# Create an empty DataFrame to store the historical returns
historical_returns = pd.DataFrame()

# Iterate through each ticker and fetch historical data
for ticker in tickers:
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date)
    

    # Calculate quarterly returns
    quarterly_returns = data['Adj Close'].ffill().pct_change()
    #quarterly_returns = data['Adj Close'].resample('Q').ffill().pct_change()

    # Append to the historical_returns DataFrame
    historical_returns[ticker] = quarterly_returns

# Export the DataFrame to an Excel file
file_name = FILE_NAME
historical_returns.to_excel((file_name+'.xlsx'), index=True)


