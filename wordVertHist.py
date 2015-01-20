import cv2
import numpy as np

def drawVertHist(List_Word_Details, thresh_No_DE):

	fileWordVertHist = open('WordVertHist2.txt', 'w')
	
	for word in List_Word_Details:
		BWx = word['BWx']
		#BWy = word['BWy']
		BWy = word['HS']
		EWx = word['EWx']
		EWy = word['EWy']
		col_sum = 0
		list_Word_Vert_Hist = []
		fileWordVertHist.write("\n\nLine no.: %d,  Word no. %d begins..............\n" % (word['lineNo'], word['wordNo']))
		fileWordVertHist.write("\nHeader width: %d" % (word['hw']))
		for x in range(BWx, EWx+1):
			for y in range(BWy, EWy+1):
				pixel = thresh_No_DE[y,x]

				if(pixel==255):
					col_sum += 1

			list_Word_Vert_Hist.append(col_sum)
			#print no. of pixels==255 in each row
			fileWordVertHist.write("\ncol: %d = %d" % (x, col_sum))
			col_sum = 0
	fileWordVertHist.close()