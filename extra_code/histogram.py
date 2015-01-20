import cv2
import numpy as np
from matplotlib import pyplot as plt

def plotHist(img):
	
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	hist1 = cv2.calcHist([gray],[0],None,[256],[0,256])
	fileHist = open('hist.txt','w')
	fileHist.write("pixel_value:   No. of pixels\n")
	count =0 
	hist = []
	for item in hist1:
		hist.append(item)
		fileHist.write("%d:  %d\n" % (count, item))
		count += 1

	fileHist.close()
	
	#draw histogram graph
	#plt.hist(gray.ravel(),256,[0,256])
	#plt.show()
	return hist