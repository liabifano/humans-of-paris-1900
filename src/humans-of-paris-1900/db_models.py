from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, schema

db = SQLAlchemy()


def serialize(d, keys):
    return {c: getattr(d, c) for c in inspect(d).attrs.keys() if c in keys}


class Inputs(db.Model):
    __tablename__ = 'inputs'
    __table_args__ = (schema.UniqueConstraint('image_id'), )

    image_id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    request_time = db.Column(db.DateTime, nullable=False)
    path = db.Column(db.String, nullable=False)


    def __repr__(self):
        return '<Inputs {}>'.format(self.image_id)
