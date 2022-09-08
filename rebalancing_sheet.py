from typing import Union
import pandas as pd
import numpy as np


def rebalancer(initial_cash: float, prices_dict: dict) \
        -> Union[str, float]:
    """
    :param initial_cash: Scalar value must be float or convertible to
    float
    :param prices_dict: Key value pair of equal length containing 2 keys
    "Share Price" and "Current Price".
    :return: JSON object for table to be presented along with two
    scalars cash_after_initial_allocation and
    current_portfolio_return_marked_to_market
    """
    # Convert initial cash to float
    try:
        initial_cash = float(initial_cash)
    except ValueError:
        raise ValueError("Initial cash amount should be float or int")

    # Parse user input on Share Price
    try:
        conv_share_price = [float(i) for i in prices_dict['Share Price']]
        prices_dict['Share Price'] = conv_share_price
    except ValueError:
        raise ValueError("Share Price should be float or int")

    # Parse user input on Current Price
    try:
        conv_current_price = [float(i) for i in
                              prices_dict['Current Price']]
        prices_dict['Current Price'] = conv_current_price
    except ValueError:
        raise ValueError("Current Price should be float or int")

    # Parse input shape
    if len(prices_dict['Current Price']) != \
            len(prices_dict['Share Price']):
        raise ValueError('Length of Current Price '
                         'must equal Share Price')

    df = pd.DataFrame(data=prices_dict)
    df['# of Shares'] = np.floor(
        (initial_cash / len(prices_dict['Share Price'])) /
        df['Share Price'])
    df['initial cost'] = df['# of Shares'] * df['Share Price']
    df['current value'] = df['# of Shares'] * df['Current Price']
    df['P&L %  +/-'] = np.round(
        ((df['Current Price'] / df['initial cost']) - 1) * 100, 2)
    df['Target'] = (initial_cash / len(prices_dict['Share Price']))
    df['Rebalancing'] = df['current value'] - df['Target']

    df = df[
        ['# of Shares', 'Share Price', 'initial cost',
         'Current Price', 'current value', 'P&L %  +/-',
         'Rebalancing', 'Target']]

    cash_after_initial_allocation = initial_cash - df[
        'initial cost'].sum()
    current_portfolio_return_marked_to_market = \
        df['current value'].sum() - df['initial cost'].sum()

    df = df.round(2)
    cash_after_initial_allocation = cash_after_initial_allocation.\
        round(2)
    current_portfolio_return_marked_to_market = \
        current_portfolio_return_marked_to_market.round(2)

    df = df.to_json()

    return df, cash_after_initial_allocation, \
           current_portfolio_return_marked_to_market
