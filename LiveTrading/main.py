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
    """
    :param api: Alpaca API
    :return: None
    """

    account = api.get_account()
    print(f'''
    Account ID: {account.id}
    Account Equity: {account.equity}
    Account Status: {account.status}
    ''')

    # Check how much money we can use to open new positions.
    print('${} is available as buying power.'.format(account.buying_power))


def validate_trade(api: tradeapi.rest.REST, ticker: str, trade: str, amount: float):
    """
    :param api: Alpaca API
    :param ticker: stock ticker
    :param trade: buy/sell
    :param amount: amount to be bought or sold
    :return: True if all checks passed, False otherwise
    """
    account = api.get_account()

    cash = float(account.buying_power)
    max_position = 0.05*cash
    # latest traded price
    stock_price = api.get_latest_trade(ticker).price
    position_size = stock_price * abs(amount)

    checks = {
        position_size > max_position: 'Position size is too large, trade will not be executed.',
        account.trading_blocked: 'Account is currently restricted from trading.'
    }

    failed_check = next((msg for condition, msg in checks.items() if condition), None)

    if failed_check:
        print(failed_check)
        return False

    print('All checks passed')
    return True


if __name__ == '__main__':
    trade_api = connect_api()

    sample_trade = {'AAPL': 0.5, 'AMZN': -1}

    for stock, quantity in sample_trade.items():
        # determine whether to buy or sell:
        if quantity > 0:
            action = 'buy'
        else:
            action = 'sell'

        # implement some safety checks here, do we have enough money, does order make sense...
        if validate_trade(trade_api, stock, action, quantity) is True:
            # print basic information
            print(f'stock: {stock}, {action}: {abs(quantity)}')

            # send order to API
            order = execute_order(trade_api, stock, abs(quantity), action)

            # print order information
            print(order)
        else:
            print('Trade could not be executed, check input.')
