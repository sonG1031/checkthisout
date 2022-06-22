from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable=False)
    student_id = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    checked = db.Column(db.Boolean, default=False, nullable=True)

class SelfCheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.String(200), nullable=False) # 경로만 저장
    student_id = db.Column(db.String(150), db.ForeignKey('user.student_id', ondelete='CASCADE'), nullable=False)
    user = db.relationship("User", backref=db.backref("self_check_set", cascade='all, delete-orphan'))