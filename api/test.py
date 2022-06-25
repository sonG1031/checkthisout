import cv2
import pytesseract
from PIL import Image
import numpy as np
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'

b = cv2.imread('../images/userImgs/21213.jpeg', cv2.IMREAD_GRAYSCALE)
# _, binary = cv2.threshold(b, 127, 255, cv2.THRESH_BINARY)
# out = binary.copy()
# out = 255 - out
img_blurred = cv2.GaussianBlur(b, ksize=(0,0), sigmaX=1)
img_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)

cv2.imshow('img', img_thresh)
cv2.waitKey()
now = datetime.now().strftime('%Y-%m-%d')
result = pytesseract.image_to_string(img_thresh, lang='kor')
print(result)