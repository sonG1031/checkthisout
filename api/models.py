from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable =False)

class SelfCheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.String(200), nullable=False) # 경로만 저장
    user_name = db.Column(db.String(150), db.ForeignKey('user.username', ondelete='CASCADE'), nullable=False)
    user = db.relationship("User", backref=db.backref("job_notice_set", cascade='all, delete-orphan'))