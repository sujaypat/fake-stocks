import unittest
import os
import requests


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


if __name__ == '__main__':
    unittest.main()
