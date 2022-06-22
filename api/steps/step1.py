# 자가진단 화면인지 검사
import cv2
from skimage.metrics import structural_similarity as ssim

def isSelfCheck(path):
    imgA = cv2.imread('images/a.jpeg')
    imgB = cv2.imread(f'{path}')

    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    try:
        score, diff = ssim(grayA, grayB, full=True)
        if score > 
    except:



try:
    (score1, diff1) = ssim(grayA, grayT, full=True)
    diff1 = (diff1 * 255).astype("uint8")
    print(score1)
except:
    print("이미지 비교에 문제가 생겼습니다.")
