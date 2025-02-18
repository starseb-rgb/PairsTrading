import configparser
import alpaca_trade_api as tradeapi

config = configparser.ConfigParser()
config.read('config.ini')


def connect_api():
    """
    Connect to Alpaca Trading API
    Config file needs to added manually since it is ignored as stated in .gitignore
    :return: api connection
    """
    base_url = config['ALPACA']['ENDPOINT']
    api_key = config['ALPACA']['API_KEY']
    secret_key = config['ALPACA']['SECRET_KEY']

    api = tradeapi.REST(key_id=api_key,
                        secret_key=secret_key,
                        base_url=base_url,
                        api_version='v2')
    return api


def execute_order(api: tradeapi.rest.REST,
                  ticker: str,
                  qty: float,
                  side=str,
                  order_type='market',
                  time_in_force='day'):
    """
    executes buy order
    :param api: alpaca REST api connection
    :param ticker: ticker symbol
    :param qty: how much to buy
    :param side: buy/sell
    :param order_type: execute immediately at best available price
    :param time_in_force: gtc = good til canceled
    :return: info about order
    """
    order = api.submit_order(
        symbol=ticker,
        qty=qty,
        side=side,
        type=order_type,
        time_in_force=time_in_force
    )
    return order


def info(api: tradeapi.rest.REST):

    account = api.get_account()
    print(f'''
    Account ID: {account.id}
    Account Equity: {account.equity}
    Account Status: {account.status}
    ''')


if __name__ == '__main__':
    trade_api = connect_api()

    sample_trade = {
        'AAPL': 0.5,
        'AMZN': -1
    }

    for stock, quantity in sample_trade.items():
        # determine whether to buy or sell:
        if quantity > 0:
            action = 'buy'
        else:
            action = 'sell'

        # print basic information
        print(f'stock: {stock}, {action}: {abs(quantity)}')

        # send order to API
        order = execute_order(trade_api, stock, abs(quantity), action)

        # print order information
        print(order)
