from flask import request, jsonify
from flask_restx import Resource, Namespace
from api.route.auth import login_required
from api.steps import *


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
                print("모든 검증을 통과하셨어요!!")
            else:
                print("다시시도")
        else:
            print("다시시도")
            # return jsonify({'msg': -1})

        # 1. 받아온 사진을 a.jpeg 파일과 비교하여 유효성 검사
        # 2. 사진에서 글자 추출
        # 3. 추출한 글자를 이용해 db에 상태 저장
        # 4. 유효성 검사 통과시 코드 전송, 실패시 다시 시도