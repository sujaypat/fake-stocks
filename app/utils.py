import requests
import json


def get_data_for_symbol(ticker):
    """
    :param ticker: string of ticker symbol
    :return: tuple with status code and response json
    """
    url = 'https://finance.google.com/finance?q=%s&output=json' % ticker
    response = requests.get(url)
    return response.status_code, json.loads(response.text)
