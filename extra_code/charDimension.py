import cv2
import numpy as np

def calculateCharDimension(List_Char_Details):

	fileCharDim = open('CharDimension_Refined.txt','w')
	fileCharDim.write("\n\n********Character Width-Height Details*************************\n\n")
	count = 0
	for char in List_Char_Details:

		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
		charWidth = char['ECx'] - char['BCx'] + 1
		charHeight = char['ECy'] - char['BCy'] + 1

		#Adding new entry in the dictionary
		char['width'] = charWidth
		char['height'] = charHeight
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number, hw: header_width
		#width: Char Width, height: CHar Height

		fileCharDim.write("\nline no.: %d,  word no.:%d, char no.: %d,  height:  %d, width:  %d,  headerWidth: %d" % (char['lineNo'], char['wordNo'], char['charNo'], charHeight, charWidth, char['hw']))
		count += 1

	seq_Char_Width = [x['width'] for x in List_Char_Details]
	seq_Char_Height = [x['height'] for x in List_Char_Details] 

	mean_width = np.mean(seq_Char_Width)
	mean_height = np.mean(seq_Char_Height)
	
	fileCharDim.write("\n\n\nMax Width: %d,   Min Width: %d,  Mean Width: %d\n" % (max(seq_Char_Width), min(seq_Char_Width), mean_width))
	fileCharDim.write("\nMax Height: %d,   Min Height: %d,  Mean Height: %d\n" % (max(seq_Char_Height), min(seq_Char_Height), mean_height))

	fileCharDim.close()

	return List_Char_Details, mean_width, mean_height


