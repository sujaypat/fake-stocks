import unittest
import requests
from app import app, utils


class TestAPIMethods(unittest.TestCase):

    def test_index(self):
        r = requests.get('http://127.0.0.1:5000')
        assert(r.status_code == 200)

    def test_login_page(self):
        r = requests.get('http://127.0.0.1:5000/login')
        print(r.content)
        assert(r.status_code == 200)

    def test_login(self):
        r = requests.get('http://127.0.0.1:5000/login')
        p = requests.post('http://127.0.0.1:5000/submit', data={'username': 'hjkl', 'password': 'hjkl'})
        print(p.content)
        assert(p.status_code == 200)

    def test_create(self):
        r = requests.get('http://127.0.0.1:5000/login')
        p = requests.post('http://127.0.0.1:5000/create', data={'create_username': 'qwerty', 'create_password': 'qwerty'})
        print(p.content)
        assert(p.status_code == 200)

    def test_funds(self):
        l = requests.post('http://127.0.0.1:5000/submit', data={'username': 'hjkl', 'password': 'hjkl'})
        assert(l.status_code == 200)

        add = requests.post('http://127.0.0.1:5000/funds', data={'funds_amt': 10})
        # assert(add.status_code == 200)

        u = utils.username_exists('hjkl')
        assert(u is not None)
        assert(u.bank_balance >= 0)

    def test_buy(self):
        with app.test_client() as client:
            l = client.post('/submit', data={'username': 'hjkl', 'password': 'hjkl'})
            assert(l.status_code == 200)

            # with client.session_transaction() as sess:
            # print(flask.request.args['user'])
            buy = client.post('/buy', data={'buy_ticker': 'aapl', 'buy_num': '1'})
            # assert(buy.status_code == 200)

    def test_sell(self):
        with app.test_client() as client:
            l = client.post('/submit', data={'username': 'hjkl', 'password': 'hjkl'})
            assert(l.status_code == 200)

            # with client.session_transaction() as sess:
            # print(flask.request.args['user'])
            sell = client.post('/sell', data={'sell_ticker': 'aapl', 'sell_num': '1'})
            # assert(buy.status_code == 200)


if __name__ == '__main__':
    unittest.main()
