import os
import cv2
import easyocr

from datetime import datetime

from api.models import User


def step1(img_path):
    a = cv2.imread('./images/a.jpeg')
    b = cv2.imread(img_path)

    a_hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
    b_hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)


    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges
    channels = [0, 1]

    hist_a = cv2.calcHist([a_hsv], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_a, hist_a, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    hist_b = cv2.calcHist([b_hsv], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_b, hist_b, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    score = cv2.compareHist(hist_a, hist_b, cv2.HISTCMP_CHISQR_ALT)
    print(score)
    if score < 1.5:
        print("자가진단 화면")
        return True
    else :
        print("다른 화면")
        os.remove(img_path)
        return False


def step2(img_path, student_id):

    reader = easyocr.Reader(['ko'], gpu=True)

    result = reader.readtext(img_path)
    os.remove(img_path)
    now = datetime.now().strftime('%Y-%m-%d')
    user = User.query.filter_by(student_id= student_id).first()
    cnt = [0, 0]

    for _, text, _ in result:
        print(text)
        for char in user.username:
            if char in text:
                cnt[0] += 1
                print(text)
        if now in text:
            cnt[1] += 1

    print(cnt)
    if cnt[0] >= 1 and cnt[1] >= 1:
        return True
    else:
        return False


