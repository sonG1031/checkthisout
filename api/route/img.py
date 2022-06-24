from flask import request, jsonify
from flask_restx import Resource, Namespace
# from api.models import
from api.route.auth import login_required
from api import db
from datetime import datetime
from api.steps import step1


img = Namespace("image")

@img.route('')
class Image(Resource):
    @login_required
    def post(self):
        # print(request.files['image'])
        # print(request.headers['student_id'])
        img = request.files['image']
        # print(type(img))
        path = f"./images/userImgs/{request.headers['student_id']}.jpg"
        img.save(path)

        if step1(path):
            return jsonify({"msg":"good"})

        # 1. 받아온 사진을 a.jpeg 파일과 비교하여 유효성 검사
        # 2. 사진에서 글자 추출
        # 3. 추출한 글자를 이용해 db에 상태 저장
        # 4. 유효성 검사 통과시 코드 전송, 실패시 다시 시도