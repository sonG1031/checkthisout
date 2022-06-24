import os
import cv2
import numpy as np


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
    if score < 1.0:
        print("자가진단 화면")
        return True
    else :
        print("다른 화면")
        os.remove(img_path)
        return False