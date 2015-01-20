from skimage import morphology
import numpy as np
import cv2
import thinning

'''
im = cv2.imread("athva.jpg")
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU)[1]
im = cv2.dilate(im,None,iterations = 3)
im = cv2.erode(im,None,iterations = 2)
im = morphology.skeletonize(im > 0)
im1 = im.astype(np.uint8)*255 
cv2.imwrite("dst.jpg", im1)
'''

src = cv2.imread("bhug.png")
if src == None:
	sys.exit()
bw = cv2.cvtColor(src, cv2.cv.CV_BGR2GRAY)
_, bw2 = cv2.threshold(bw, 10, 255, cv2.THRESH_BINARY)
bw2 = thinning.thinning(bw2)
cv2.imshow("src", bw)
cv2.imshow("thinning", bw2)
cv2.waitKey()