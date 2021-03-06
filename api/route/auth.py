from flask import request, jsonify, Response, json, Blueprint
from flask_restx import Resource, Namespace, abort

from api import db
from api.models import User, SelfCheck

import bcrypt, jwt
from config import JWT_SECRET_KEY, IS_CAM_KEY
from functools import wraps
from datetime import datetime

auth = Namespace('auth')


@auth.route('/signup/')
class Signup(Resource):
    def post(self):
        user = User.query.filter_by(student_id = request.json["student_id"]).first()
        if not user:
            student_id = request.json['student_id']
            username = request.json['username']
            password = bcrypt.hashpw(request.json['password'].encode("utf-8"), bcrypt.gensalt())
            user = User(username=username,
                        password=password.decode('utf-8'),
                        student_id=student_id
                        )

            db.session.add(user)
            db.session.commit()
            db.session.remove()
            return jsonify({
                'code': 1,
                'msg' : "회원가입 성공!",
                'data':{}
            })
        else:
            return jsonify({
                'code': -1,
                'msg': "회원가입 실패!",
                'data': {}
            })

@auth.route('/login/')
class Login(Resource):
    def post(self):
        error = None
        user = User.query.filter_by(student_id=request.json['student_id']).first()

        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password.encode('utf-8')):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            payload = {
                "student_id": user.student_id,
                "password": user.password
            }
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
            print(token)
            body = json.dumps({
                "code": 1,
                "msg": "로그인에 성공하셨습니다.",
                "data": {
                    "id" : user.id,
                    "username" : user.username,
                    "password": user.password,
                    "student_id": user.student_id
                }
            }, ensure_ascii=False)

            qr = SelfCheck.query.filter_by(student_id= user.student_id).first()
            if qr :
                today = datetime.today().strftime('%Y-%m-%d')
                qrDate = qr.date.strftime('%Y-%m-%d')
                diff = str(datetime.now() - qr.date)[:7].split(":")

                if today != qrDate or int(diff[0]) > 2:
                    db.session.delete(qr)
                    user.checked = False
                    db.session.commit()

            db.session.remove()
            response = Response(body)
            response.headers['authorization'] = token
            return response
        return jsonify({
            "code": -1,
            "msg": error,
            "data": {}
        })


# 토큰 검증을 위한 함수들
def check_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, "HS256")
    except jwt.InvalidTokenError:
        payload = None
    return payload

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        token = request.headers.get('authorization')
        isCam = request.headers.get('camera_request')

        if isCam == IS_CAM_KEY: # cam이 보낸 요청인지 확인함.
            print("cam!!")
            return f(*args, **kwagrs)

        if token is not None:
            payload = check_token(token)
            if payload is None:
                abort(401, message="토큰 검증에 실패하셨습니다.")
        else:
            abort(401, message="토큰 검증에 실패하셨습니다.")
        return f(*args, **kwagrs)
    return decorated_function

