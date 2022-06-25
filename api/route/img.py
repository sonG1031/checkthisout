from flask import request, jsonify
from flask_restx import Resource, Namespace

from api.models import SelfCheck
from api import db
from api.route.auth import login_required
from api.steps import *
import random
import string

img = Namespace("image")

@img.route('')
class Image(Resource):
    @login_required
    def post(self):
        # print(request.files['image'])
        # print(request.headers['student_id'])
        img = request.files['image']
        # print(type(img))
        path = f"./images/userImgs/{request.headers['student_id']}.jpeg"
        img.save(path)

        user = User.query.filter_by(student_id=request.headers['student_id']).first()

        if step1(path):
            if step2(path, user.student_id):
                if user.checked:
                    print("이미 코드를 받으셨습니다.")
                    return jsonify({'data': -1})

                lower = string.ascii_lowercase
                upper = string.ascii_uppercase
                num = string.digits
                symbols = string.punctuation

                all = lower + upper + num + symbols

                # code = None
                while True:
                    tmp = random.sample(all, 15)
                    code = r"".join(tmp)
                    exist_check = SelfCheck.query.filter_by(code= code).first()
                    if not exist_check:
                        db.session.add(SelfCheck(student_id= user.student_id, code= code))
                        user.checked = True
                        db.session.commit()
                        break

                db.session.remove()
                print("모든 검증을 통과하셨어요!!")
                return jsonify({'data': 1})

        print("다시시도")
        return jsonify({'data': -1})

        # 1. 받아온 사진을 a.jpeg 파일과 비교하여 유효성 검사
        # 2. 사진에서 글자 추출
        # 3. 추출한 글자를 이용해 db에 상태 저장
        # 4. 유효성 검사 통과시 코드 전송, 실패시 다시 시도


@img.route('/qr/<string:student_id>/')
class QrCode(Resource):
    @login_required
    def get(self, student_id):
        qr = SelfCheck.query.filter_by(student_id= student_id).first()
        return jsonify({'data': qr.code})


@img.route('/cam/<string:code>')
class Cam(Resource):
    @login_required
    def get(self, code):
        qr = SelfCheck.query.filter_by(code=code).first()
        if qr:
            return jsonify({'data': 'success'})
        else :
            return jsonify({'data': 'failed'})

