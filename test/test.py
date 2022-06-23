import cv2
import numpy as np
a = cv2.imread('a.jpeg')
test = cv2.imread('test7.jpeg')


a_hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
test_hsv = cv2.cvtColor(test, cv2.COLOR_BGR2HSV)

h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]
h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges
channels = [0, 1]

hist_a = cv2.calcHist([a_hsv], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_a, hist_a, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

hist_test = cv2.calcHist([test_hsv], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_test, hist_test, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

a_test = cv2.compareHist(hist_a, hist_test, cv2.HISTCMP_BHATTACHARYYA)
# a_test = a_test / np.sum(hist_a)
print(a_test)

cv2.imshow('a', a)
cv2.imshow('test',test)

cv2.waitKey(0)
