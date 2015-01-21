import cv2
import numpy as np


def removeEmptyChars(img, List_Char_Details_Refined):

	List_Char_Details_Final = []

	for char in List_Char_Details_Refined:
		#crop and get each character
		height = char['ECy'] - char['BCy'] + 1
		width = char['ECx'] - char['BCx'] + 1
		if(height > 1 and width > 1):
			List_Char_Details_Final.append(char)

	print("No. of non-empty characters:\n" + str(len(List_Char_Details_Final)))
	return List_Char_Details_Final



def removeHeaderLine(List_Char_Details_Refined):
	for char in List_Char_Details_Refined:
		if(char['region']==2):
			char['BCy'] += char['hw']


def downsample(img, List_Char_Details_Refined, resized_Width, resized_Height):

	fileCharData = open('CharData.csv','w')

	for char in List_Char_Details_Refined:
		
		fileCharData.write("lineNo: %d,  wordNo: %d, region: %d,  charNo: %d, width: %d, height: %d" % (char['lineNo'], char['wordNo'], char['region'], char['charNo'], char['ECx']-char['BCx']+1, char['ECy']-char['BCy']+1))
		#crop and get each character
		crop_char = img[char['BCy']:char['ECy'], char['BCx']:char['ECx']]

		#resize each character
		resized_char = cv2.resize(crop_char, (resized_Width, resized_Height))

		#convert resized character to binary
		gray = cv2.cvtColor(resized_char,cv2.COLOR_BGR2GRAY)
		ret,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
		
		#pixel = thresh[19,14]
		for y in range(0, resized_Height):
			for x in range(0, resized_Width):
				#print("col: " + str(y) + ", row: " + str(x))
				pixel = thresh[y,x]
				value = 0
				if(pixel == 255):
					value = 1
				fileCharData.write(", %d" % value)
		fileCharData.write("\n")
	fileCharData.close()
