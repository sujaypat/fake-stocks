import requests
import json
import hashlib
from app import models
import matplotlib.pyplot as plt
import base64

API_KEY = 'Y7NVICPUUJESAGD0'


def get_data_for_symbol(ticker):
    """
    :param ticker: string of ticker symbol
    :return: tuple with status code and response json
    """
    url = 'http://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=5min&symbol=%s&apikey=%s' % (ticker.lower(), API_KEY)
    response = requests.get(url)
    print(url)
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
    """

    :param ticker: stock ticker
    :return: latest price for that ticker on 5 min interval
    """
    resp, data = get_data_for_symbol(ticker)
    print(resp)
    print(data[0][1]['4. close'])
    return float(data[0][1]['4. close'])


def gen_chart(historical, share):
    _, resp = get_data_for_symbol(share.ticker)
    templist = [x for x in resp[::-1]]
    for i in range(len(templist)):
        templist[i] = (templist[i][0], float(templist[i][1]['4. close']))
    labels = [a for (a, b) in templist[::2]]
    values = [b for (a, b) in templist[::2]]
    plt.figure(figsize=(10, 6))
    x = range(len(values))
    plt.xticks(range(len(values)), labels, rotation=90)  # writes strings with 45 degree angle
    plt.plot(x, values)
    plt.title('%s historical plot' % share.ticker)
    plt.tight_layout()

    from io import BytesIO
    figure = BytesIO()
    plt.savefig(figure, format='png')
    figure.seek(0)
    figdata_png = base64.b64encode(figure.getvalue())
    historical.append(figdata_png.decode('utf8'))
