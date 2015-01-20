import cv2
import numpy as np

def ExtractWords(img, thresh, List_Line_Details, pixel_Limit_Word_Extraction):

	max_y, max_x, depth = img.shape

	#write pixel sum details in a file
	#####fileExtractWord = open('extractWord_No_DE.txt','w')
	lineCount = 0

	List_Word_Details = []

	for line in List_Line_Details:

		beginLine = line['LB']
		endLine = line['LE']

		#####fileExtractWord.write("\n\nLine no. %d begins..............\n" % (lineCount))
		col_sum = 0
		list_col_sum = []

		#noOfColumns = endLine - beginLine + 1
		for x in range(0, max_x):
			for y in range(beginLine, endLine):
				pixel = thresh[y,x]

				if(pixel==255):
					col_sum += 1

			list_col_sum.append(col_sum)
			#print no. of pixels==255 in each row
			#####fileExtractWord.write("col: %d = %d\n" % (x, list_col_sum[x]))
			col_sum = 0

		length_col_sum = len(list_col_sum)

		i = 0
		wordCount = 0
		while(i < length_col_sum):
			if(list_col_sum[i] > pixel_Limit_Word_Extraction):
				list_word = []
				for j in range(i, length_col_sum):
					if( list_col_sum[j] > pixel_Limit_Word_Extraction):
						list_word.append(j)

					else:
						break

				Dict = {'BWx': list_word[0], 'BWy' : beginLine, 'EWx': list_word[-1], 'EWy': endLine, 'lineNo': lineCount, 'wordNo': wordCount}
				#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
				#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number
				List_Word_Details.append(Dict)
				wordCount += 1

				i += len(list_word)
			else:
				i += 1

		
		lineCount += 1

	#####fileExtractWord.close()

	print "No. of words: "
	print len(List_Word_Details)
	return List_Word_Details