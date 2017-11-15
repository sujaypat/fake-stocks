import requests
import json
import hashlib
from app import models


def get_data_for_symbol(ticker):
    """
    :param ticker: string of ticker symbol
    :return: tuple with status code and response json
    """
    url = 'https://finance.google.com/finance?q=%s&output=json' % ticker
    response = requests.get(url)
    # print(response.text.strip()[3:])
    return response.status_code, json.loads(response.text.strip()[3:])


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
