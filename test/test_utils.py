import unittest
import os
from config import basedir
from app import app, db, utils
from app.models import User, Share
import hashlib


class TestUtilMethods(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_read_user_from_db(self):
        u = User(username='john', password=hashlib.sha512('qwerty'.encode('utf-8')).digest(), bank_balance=0)
        db.session.add(u)
        db.session.commit()
        u = User(username='bob', password=hashlib.sha512('uiop'.encode('utf-8')).digest(), bank_balance=0)
        db.session.add(u)
        db.session.commit()
        res = utils.read_user_from_db('john', 'qwerty')
        assert(res.password == hashlib.sha512('qwerty'.encode('utf-8')).digest())
        assert(res.bank_balance == 0)

    def test_add_read_share(self):
        s = Share(ticker='aapl', count=7, user_id=1)
        db.session.add(s)
        db.session.commit()
        res = Share.query.get(1)
        assert(res.count == 7)

    def test_get_data_for_symbol(self):
        code, resp = utils.get_data_for_symbol('AAPL')
        assert(code == 200)

    def test_get_current_price(self):
        price = utils.get_current_price('aapl')
        assert(price > 150)


if __name__ == '__main__':
    unittest.main()
