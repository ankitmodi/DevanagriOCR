import cv2
import numpy as np
import maths_func
import matplotlib.pyplot as plt

def ExtractChars(img, thresh_No_DE, List_Word_Details, pixel_Limit_Char_Extraction, header_Line_Percent):

	List_Char_Details = []

	#write pixel sum details in a file
	fileWordHorzHist = open('WordHorzHist.txt','w')
	fileExtractChar = open('extractChar.txt','w')
	wordCount = 0

	
	for word in List_Word_Details:

		#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
		#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number

		BWx = word['BWx']
		BWy = word['BWy']
		EWx = word['EWx']
		EWy = word['EWy']


		row_sum = 0
		header_width = 1
		list_Word_Hor_Hist = []


		list_Gap_Begin_x = []
		list_Gap_Begin_y = []
	
		list_Gap_End_x = []
		list_Gap_End_y = []

		fileWordHorzHist.write("\n\nLine no.: %d,  Word no. %d begins..............\n" % (word['lineNo'], word['wordNo']))


		#*******************calculate horizontal histogram of word to get width of header line***********************
		
		for y in range(BWy, EWy+1):
			for x in range(BWx, EWx+1):
				pixel = thresh_No_DE[y,x]

				if(pixel==255):
					row_sum += 1

			list_Word_Hor_Hist.append(row_sum)
			#print no. of pixels==255 in each row
			fileWordHorzHist.write("row: %d = %d\n" % (y, row_sum))
			row_sum = 0

		max_Word_Horz_Hist = max(list_Word_Hor_Hist)
		fileWordHorzHist.write("\n Maximum value: %d " % (max_Word_Horz_Hist))

		indexOfMax_Word_Horz_Hist = list_Word_Hor_Hist.index(max(list_Word_Hor_Hist))
		fileWordHorzHist.write("\n Index of Max value: %d " % (indexOfMax_Word_Horz_Hist))

		#iterate below the maximum value
		temp_Max = max_Word_Horz_Hist
		temp_Index_Max = indexOfMax_Word_Horz_Hist
		header_limit = header_Line_Percent * max_Word_Horz_Hist
		fileWordHorzHist.write("\n Header limit (50 percent of max): %d " % (header_limit))

		#counting header width in forward/below direction
		for i in range(indexOfMax_Word_Horz_Hist+1, len(list_Word_Hor_Hist)):
			if (list_Word_Hor_Hist[i] > header_limit):
				header_width += 1
			else:
				break

		#counting header width in backward/above direction
		for i in range(indexOfMax_Word_Horz_Hist-1, -1, -1):
			if (list_Word_Hor_Hist[i] > header_limit):
				header_width += 1
			else:
				break

		fileWordHorzHist.write("\n Header width: %d " % (header_width))



		#*****************************************************************************************************

		

		fileExtractChar.write("\n\nLine No.: %d,  Word No.: %d begins..............\n" % (word['lineNo'], word['wordNo']))

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
			fileExtractChar.write("col: %d = %d\n" % (x, col_sum))
			col_sum = 0

		#****************Finding all the characters************

		length_col_sum = len(list_col_sum)

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

				Dict = {'BCx': BCx, 'BCy': BCy, 'ECx': ECx, 'ECy': ECy, 'lineNo': word['lineNo'], 'wordNo': word['wordNo'], 'charNo': charCount, 'hw': header_width}
				#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
				#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
				
				List_Char_Details.append(Dict)
				charCount += 1

				i += len(list_char)

			else:
				i += 1


		
		
		wordCount += 1
		#print wordCount
	#***************************************  for loop for each word ends here  ***************************************
	fileWordHorzHist.close()
	fileExtractChar.close()
	#print wordCount

	print "No.of characters:"
	print len(List_Char_Details)

	return List_Char_Details





def FilterCharWidth(thresh_No_DE, List_Char_Details_WH, mean_width, width_limit_percent):

	# List_Char_Details_WH IDs are as follows:
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number, splitNo: splits number in joint char else -1
	#width: Char Width, height: Char Height, hw: header_width, splitNo: if not split then -1, else the split no in joint char
	fileCharFilter = open('CharFilter.txt','w')
	fileCharCheck = open('CharCheck.txt','w')
	#fileCharSplitDim = open('CharSplitDimension.txt','w')
	#fileCharSplitDim.write("\n\n********Character Width-Height Details*************************\n\n")

	width_limit = mean_width * width_limit_percent
	fileCharCheck.write("\n\nmean width: %d,  width_limit.: %d\n" % (mean_width, width_limit))

	List_Char_Details_FCW = []

	pmc = 0.1
	#Add percent of mean width to char width before dividing with mean width, 0.1 means 10%

	mulHeader = 2
	#multiples of header for gap finding

	for char in List_Char_Details_WH:

		
		if(char['width'] <= width_limit):

			#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
			#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number,
			#width: Char Width, height: Char Height, hw: header_width, splitNo: if not split then -1, else the split no in joint char
			Dict = {'BCx': char['BCx'], 'BCy': char['BCy'], 'ECx': char['ECx'], 'ECy': char['ECy'], 'lineNo': char['lineNo'], 'wordNo': char['wordNo'], 'charNo': char['charNo'], 'width': char['width'], 'height': char['height'], 'hw': char['hw'], 'splitNo':-1}

			List_Char_Details_FCW.append(Dict)

		else:
			fileCharCheck.write("\n\n\n***********************************************************************************")
			fileCharCheck.write("\nLine No.: {0},  Word No.: {1}, Char No.: {2},  width: {3}, x_coord: {4}-{5}".format(char['lineNo'], char['wordNo'], char['charNo'], char['width'], char['BCx'], char['ECx']))
			fileCharCheck.write("\n***********************************************************************************\n\n")


			#*****find no. of splits which is one less than no. of chars this joint-char would be broken into*****
			no_of_splits = int(( char['width'] / mean_width) - 1)
			#no_of_splits = int(( char['width'] + pmc*mean_width ) / mean_width)
			#no_of_chars = no_of_splits + 1
			
			



			#**************find sums of all columns of this joint-char**************
			fileCharFilter.write("\n\nLine No.: %d,  Word No.: %d Char No.: %d\n" % (char['lineNo'], char['wordNo'], char['charNo']))
			col_sum = 0
			list_col_sum = []
			#noOfColumns = endLine - beginLine + 1
			for x in range(char['BCx'], char['ECx']+1):
				for y in range(char['BCy'], char['ECy']+1):
					pixel = thresh_No_DE[y,x]

					if(pixel==255):
						col_sum += 1

				list_col_sum.append(col_sum)
				#print no. of pixels==255 in each row
				fileCharFilter.write("col: %d = %d\n" % (x, col_sum))
				fileCharCheck.write("\ncol: %d = %d" % (x, col_sum))
				col_sum = 0

			fileCharCheck.write("\n\nno_of_splits: %d" % (no_of_splits))

			#****************Finding all the gaps and storing  indices of their mid point************

			#iterate over word to find gaps in between
			length_col_sum = len(list_col_sum)

			#plt.bar(range(0,length_col_sum), list_col_sum)
			#plt.show()

			thresh_gap = char['hw'] * mulHeader
			fileCharCheck.write("\nthresh_gap: %d" % (thresh_gap))
			list_gap_mid = []


			i = 0
			#charCount = 0
			fileCharCheck.write("\ngap_mid: ")
			while(i < length_col_sum):
				if(list_col_sum[i] <= thresh_gap):
					list_gap = []
					for j in range(i, length_col_sum):
						if( list_col_sum[j] <= thresh_gap):
							list_gap.append(j)

						else:
							break

					#gap_mid = ( gap_start + gap_mid )/ 2
					gap_mid = ( i + (i + len(list_gap)) ) / 2
					list_gap_mid.append(gap_mid)
					fileCharCheck.write(" %d" % (char['BCx'] + gap_mid))

					i += len(list_gap)

				else:
					i += 1

			#************************determining boundaries for the split**************************
			fileCharCheck.write("\nchar inside boundary: ")
			list_char_inside_boundary = []
			#the new inside boundaries created in the joint-char
			for k in range(0, no_of_splits):
				kth_mid_point = (char['width'] * (k+1)) / (no_of_splits + 1)
				#for 2 chars, kth_mid_point would be 1/2, 1. For 3 chars, 1/3,2/3,1 and so on.
				boundary_contenders_distaceWithKthMidPoint = []
				#distance of contenders in list_gap_mid with kth mid point
				for m in range(0, len(list_gap_mid)):
					boundary_contenders_distaceWithKthMidPoint.append(abs(kth_mid_point - list_gap_mid[m]))

				#the one closest to kth_mid_point is the boundary line
				index_boundary = boundary_contenders_distaceWithKthMidPoint.index(min(boundary_contenders_distaceWithKthMidPoint))
				list_char_inside_boundary.append(list_gap_mid[index_boundary])
				fileCharCheck.write(" %d" % (char['BCx'] + list_gap_mid[index_boundary]))

			#********adding the new split chars in our char list************
			#************beginX and endX are new char boundaries************
			fileCharCheck.write("\nBoundaries: ")

			for k in range(0, len(list_char_inside_boundary)+1):
				if(k == 0):
					beginX = char['BCx']
					endX = char['BCx'] + list_char_inside_boundary[0]

				elif(k == len(list_char_inside_boundary)):
					beginX = char['BCx'] + list_char_inside_boundary[-1]
					endX = char['ECx']

				else:
					beginX = char['BCx'] + list_char_inside_boundary[k-1]
					endX = char['BCx'] + list_char_inside_boundary[k]

				fileCharCheck.write("\nbeginX: '{0}',  endX: '{1}'".format(beginX, endX))


				#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
				#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number,
				#width: Char Width, height: Char Height, hw: header_width, splitNo: if not split then -1, else the split no in joint char
				Dict = {'BCx': beginX, 'BCy': char['BCy'], 'ECx': endX, 'ECy': char['ECy'], 'lineNo': char['lineNo'], 'wordNo': char['wordNo'], 'charNo': char['charNo'], 'width': char['width'], 'height': char['height'], 'hw': char['hw'], 'splitNo':k}

				List_Char_Details_FCW.append(Dict)

	fileCharFilter.close()
	fileCharCheck.close()

	print "No.of characters after split:"
	print len(List_Char_Details_FCW)

	return List_Char_Details_FCW

#'''