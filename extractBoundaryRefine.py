import cv2
import numpy as np

def refineWord(img, thresh, List_Word_Details_Unrefined):

	for word in List_Word_Details_Unrefined:


		#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
		#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number
		BWx = word['BWx']
		BWy = word['BWy']
		EWx = word['EWx']
		EWy = word['EWy']

		while(rowSum(thresh, BWy, BWx, EWx) == 0):
			BWy += 1
		word['BWy'] = BWy

		while(rowSum(thresh, EWy, BWx, EWx) == 0):
			EWy -= 1
		word['EWy'] = EWy

	return List_Word_Details_Unrefined



def refineChar(img, thresh, List_Char_Details_Unrefined):

	
	for char in List_Char_Details_Unrefined:


		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
		BCx = char['BCx']
		BCy = char['BCy']
		ECx = char['ECx']
		ECy = char['ECy']

		while(rowSum(thresh, BCy, BCx, ECx) == 0):
			BCy += 1
		char['BCy'] = BCy

		while(rowSum(thresh, ECy, BCx, ECx) == 0):
			ECy -= 1
		char['ECy'] = ECy

	return List_Char_Details_Unrefined



def rowSum(thresh, y, BWx, EWx):
	rowSum = 0
	for x in range(BWx, EWx+1):
		pixel = thresh[y,x]
		if(pixel==255):
			rowSum += 1
	return rowSum