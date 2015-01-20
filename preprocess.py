import cv2
import numpy as np

#A function for initial preprocessing of the image
def InitialPreprocess(img):
	# convert to grayscale
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# smooth the image to avoid noises
	#gray = cv2.medianBlur(gray,5)

	# Apply adaptive threshold
	#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
	#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	#thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

	#Apply simple threshold
	ret,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

	#No dilation and erosion
	thresh_No_DE = thresh



	thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
	thresh_color_No_DE = cv2.cvtColor(thresh_No_DE, cv2.COLOR_GRAY2BGR)


	# apply some dilation and erosion to join the gaps
	#thresh = cv2.dilate(thresh,None,iterations = 3)
	#thresh = cv2.erode(thresh,None,iterations = 2)

	'''
	cv2.imshow('zz_preprocess_simple_thresh',thresh_color)
	cv2.imwrite('zz_preprocess_simple_thresh.jpg',thresh_color)
	cv2.imshow('zz_preprocess_simple_thresh_No_DE',thresh_color_No_DE)
	cv2.imwrite('zz_preprocess_simple_thresh_No_DE.jpg',thresh_color_No_DE)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''

	return thresh, thresh_No_DE, thresh_color
