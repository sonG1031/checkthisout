import cv2
from skimage.metrics import structural_similarity as ssim

imgA = cv2.imread('images/a.jpeg')
imgB = cv2.imread('images/userImgs/b.jpeg')
test = cv2.imread('test3.jpeg')
test = cv2.resize(test, (735, 1440), interpolation=cv2.INTER_LINEAR)

grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)
grayT = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

print(grayA.shape)
print(grayB.shape)
print(grayT.shape)

try:
    (score1, diff1) = ssim(grayA, grayT, full=True)
    diff1 = (diff1 * 255).astype("uint8")
    print(score1)
except:
    print("이미지 비교에 문제가 생겼습니다.")

