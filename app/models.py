from app import db


class User(db.Model):
    id = db.Column(db.Integer, index=True)
    username = db.Column(db.String(120), index=True, unique=True, primary_key=True)
    bank_balance = db.Column(db.Integer)
    password = db.Column(db.String(64), index=True)
    shares = db.relationship('Share', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


class Share(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    ticker = db.Column(db.String(4), index=True)
    value = db.Column(db.Float)
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Share %r>' % self.ticker
