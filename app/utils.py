import requests
import json
import hashlib
from app import models, db

API_KEY = 'Y7NVICPUUJESAGD0'


def get_data_for_symbol(ticker):
    """
    :param ticker: string of ticker symbol
    :return: tuple with status code and response json
    """
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=5min&symbol=%s&apikey=%s' % (ticker, API_KEY)
    response = requests.get(url)
    return response.status_code, list(json.loads(response.text.strip())['Time Series (5min)'].items())


def read_user_from_db(username, entered_password):
    """
    :param username: username to query
    :param entered_password: password to compare hash
    :return:
    """
    u = models.User.query.get(username)
    if u and u.password == hashlib.sha512(entered_password.encode('utf-8')).digest():
        return u
    return None


def username_exists(username):
    """
    :param username: username to query
    :return: whether a user with the given username exists
    """
    u = models.User.query.get(username)
    if u:
        return u
    return None


def get_current_price(ticker):
    resp, data = get_data_for_symbol(ticker)
    print(resp)
    print(data[0][1]['4. close'])
    return float(data[0][1]['4. close'])


def buy_stock(username, ticker, num_shares):
    u = username_exists(username)
    price = get_current_price(ticker)
    if not u:
        return False

    shares = u.shares.query.get(ticker=ticker)
    if u.bank_balance > price*num_shares:
        shares.count += num_shares
        u.bank_balance -= price*num_shares
        db.session.commit()


def sell_stock(username, ticker, num_shares):
    u = username_exists(username)
    price = get_current_price(ticker)
    if not u:
        return False

    shares = u.shares.query.get(ticker=ticker)
    if u.shares > num_shares:
        shares.count -= num_shares
        u.bank_balance += num_shares*price
        db.session.commit()
        return True
