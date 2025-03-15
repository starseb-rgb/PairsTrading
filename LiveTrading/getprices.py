import requests
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['ALPACA']['API_KEY']
API_SECRET = config['ALPACA']['SECRET_KEY']

def get_price(ticker_df):

    new_prices_df = pd.DataFrame(columns=['Ticker', 'Price', 'Timestamp'])

    for ticker in ticker_df['Ticker']:
        url = f"https://data.alpaca.markets/v2/stocks/{ticker}/quotes/latest"
        headers = {
            "APCA-API-KEY-ID": API_KEY,
            "APCA-API-SECRET-KEY": API_SECRET
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            new_prices_df.loc[len(new_prices_df)] = [ticker, data['quote']['ap'], data['quote']['t']]
        else:
            new_prices_df.loc[len(new_prices_df)] = [ticker, 0, f"Error: {response.status_code}, {response.text}"]

    return new_prices_df, new_prices_df.iloc[-1, -1]


if __name__ == "__main__":
    sp500_df = pd.read_csv('sp500tickers_short.csv')

    print('Ok1')

    out_df, time = get_price(sp500_df)
    filename = f"sp500_prices_{time}.csv"
    out_df.to_csv(filename, index=False)

    print('Ok2')

