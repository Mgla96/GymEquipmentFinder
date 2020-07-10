from . import db
from sqlalchemy.dialects.postgresql import JSON


class Bars(db.Model):
    __tablename__ = 'Bars'
    name = db.Column(
        db.String(100),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    brand = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    link = db.Column(
        db.String(160),
        index=True,
        unique=True,
        nullable=False
    )
    price = db.Column(
        db.String(12),
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
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    def __repr__(self):
        return '<Bars {}>'.format(self.name)

class Plates(db.Model):
    __tablename__ = 'Plates'
    name = db.Column(
        db.String(100),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    brand = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    link = db.Column(
        db.String(160),
        index=True,
        unique=True,
        nullable=False
    )
    price = db.Column(
        db.String(12),
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
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    def __repr__(self):
        return '<Plates {}>'.format(self.name)

class Racks(db.Model):
    __tablename__ = 'Racks'
    name = db.Column(
        db.String(100),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    brand = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    link = db.Column(
        db.String(160),
        index=True,
        unique=True,
        nullable=False
    )
    price = db.Column(
        db.String(12),
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
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    def __repr__(self):
        return '<Racks {}>'.format(self.name)

class Dumbbells(db.Model):
    __tablename__ = 'Dumbbells'
    name = db.Column(
        db.String(100),
        index=False,
        unique=True,
        nullable=False,
        primary_key=True
    )
    brand = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    link = db.Column(
        db.String(160),
        index=True,
        unique=True,
        nullable=False
    )
    price = db.Column(
        db.String(12),
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
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    def __repr__(self):
        return '<Dumbbells {}>'.format(self.name)

