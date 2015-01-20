import cv2
import numpy as np
#import maths_func
#import matplotlib.pyplot as plt

def ExtractChars(img, thresh_No_DE, List_Word_Split_Region):

	List_Char_Details = []

	#write pixel sum details in a file
	#fileWordHorzHist = open('WordHorzHist.txt','w')
	#####fileExtractChar = open('extractChar.txt','w')
	wordCount = 0

	
	for word in List_Word_Split_Region:

		#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
		#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number

		BWx = word['BWx']
		BWy = word['BWy']
		EWx = word['EWx']
		EWy = word['EWy']

		#*****************************************************************************************************

		

		#####fileExtractChar.write("\n\nLine No.: %d,  Word No.: %d, Region: %d , hw: %d begins..............\n" % (word['lineNo'], word['wordNo'], word['region'], word['hw']))

		col_sum = 0
		list_col_sum = []

		

		#noOfColumns = endLine - beginLine + 1
		for x in range(BWx, EWx+1):
			for y in range(BWy, EWy+1):
				pixel = thresh_No_DE[y,x]

				if(pixel==255):
					col_sum += 1

			list_col_sum.append(col_sum)
			#print no. of pixels==255 in each row
			#####fileExtractChar.write("col: %d = %d\n" % (x, col_sum))
			col_sum = 0

		#****************Finding all the characters************

		length_col_sum = len(list_col_sum)
		header_width = word['hw']
		i = 0
		charCount = 0
		while(i < length_col_sum):
			if(list_col_sum[i] > header_width):
				list_char = []
				for j in range(i, length_col_sum):
					if( list_col_sum[j] > header_width):
						list_char.append(j)

					else:
						break

				BCx = BWx + list_char[0]
				BCy = BWy
				ECx = BWx + list_char[-1]
				ECy = EWy

				Dict = {'BCx': BCx, 'BCy': BCy, 'ECx': ECx, 'ECy': ECy, 'lineNo': word['lineNo'], 
						'wordNo': word['wordNo'], 'region': word['region'], 'charNo': charCount, 
						'hw': header_width}
				#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
				#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, 
				#region: Top-Mid-Bot 1-2-3, charNo: Char Number, hw: header width(0 for Top-Bot)
				
				List_Char_Details.append(Dict)
				charCount += 1

				i += len(list_char)

			else:
				i += 1


		
		
		wordCount += 1
		#print wordCount
	#***************************************  for loop for each word ends here  ***************************************
	#fileWordHorzHist.close()
	#####fileExtractChar.close()
	#print wordCount

	print "No.of characters:"
	print len(List_Char_Details)

	return List_Char_Details