from server import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<id {}>'.format(self.id)