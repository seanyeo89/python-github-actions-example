import pandas as pd
import pytest
import yahoo_fin.stock_info as yf
from datetime import datetime, timedelta

ticker_list = yf.tickers_sp500()
ticker_list = [item.replace(".", "-") for item in ticker_list]
print(ticker_list)
start_date = datetime.now().date() - timedelta(days=5 * 365)
end_data = datetime.now().date()
df = yf.get_data(
            ticker_list[3], start_date=start_date, end_date=end_data, interval="1d")
closing_price=df['close']

##The all-time high Apple stock closing price was 179.45 on December 10, 2021
def max_close():
    return max(closing_price)

def test_close():
    assert max_close() <= 190

##Size of S&P500 IS 505 stock tickers
def test_size():
 assert len(ticker_list) == 505

def col_list():
    col_list=list(df.columns.values.tolist())
    return col_list

##7 variables of open,high,low,close,adjclose,vol etc.
def test_col():
    assert len(col_list())==7