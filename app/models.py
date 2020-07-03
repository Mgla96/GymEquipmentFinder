#from . import db

class Bars(db.Model):
    __tablename__ = 'Bars'
    name = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    link = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    price = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    image = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )
    stock = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    def __repr__(self):
        return '<Bars {}>'.format(self.name)

class Plates(db.Model):
    __tablename__ = 'Bars'
    name = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    link = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    price = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    image = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )
    stock = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    def __repr__(self):
        return '<Plates {}>'.format(self.name)

