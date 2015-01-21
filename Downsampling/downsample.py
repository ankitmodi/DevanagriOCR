import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('aa.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('thresh.jpg',thresh)
resized_image_big = cv2.resize(img, (25, 25))
cv2.imwrite('resized_image_big.jpg',resized_image_big)
