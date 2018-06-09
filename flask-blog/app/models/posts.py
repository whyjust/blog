from app.extensions import db
from datetime import datetime

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    pid = db.Column(db.Integer,default=0)
    path = db.Column(db.String(255),default='0,')
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))

