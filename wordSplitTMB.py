from __future__ import division
import cv2
import numpy as np
#import maths_func
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np










def SplitWordUpper(img, thresh_No_DE, List_Word_Details, header_Line_Percent):

	List_Word_Split_Details = []

	#write pixel sum details in a file
	#####fileWordHorzHist = open('WordHorzHist.txt','w')
	#fileExtractChar = open('extractChar.txt','w')
	wordCount = 0

	
	for word in List_Word_Details:

		#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
		#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number

		BWx = word['BWx']
		BWy = word['BWy']
		EWx = word['EWx']
		EWy = word['EWy']


		row_sum = 0
		#header_width = 1
		list_Word_Hor_Hist = []

		#####fileWordHorzHist.write("\n\nLine no.: %d,  Word no. %d..............\n" % (word['lineNo'], word['wordNo']))


		#*******************calculate horizontal histogram of word to get width of header line***********************
		
		for y in range(BWy, EWy+1):
			for x in range(BWx, EWx+1):
				pixel = thresh_No_DE[y,x]

				if(pixel==255):
					row_sum += 1

			list_Word_Hor_Hist.append(row_sum)
			#print no. of pixels==255 in each row
			#####fileWordHorzHist.write("row: %d = %d\n" % (y, row_sum))
			row_sum = 0

		max_Word_Horz_Hist = max(list_Word_Hor_Hist)
		#####fileWordHorzHist.write("\n Maximum value: %d " % (max_Word_Horz_Hist))


		indexOfMax_Word_Horz_Hist = list_Word_Hor_Hist.index(max(list_Word_Hor_Hist))
		#####fileWordHorzHist.write("\n Index of Max value: %d " % (indexOfMax_Word_Horz_Hist))

		mean_Word_Horz_Hist = np.mean(list_Word_Hor_Hist)
		#####fileWordHorzHist.write("\n Mean value: %d " % (mean_Word_Horz_Hist))


		#iterate below the maximum value
		temp_Max = max_Word_Horz_Hist
		temp_Index_Max = indexOfMax_Word_Horz_Hist
		header_limit = header_Line_Percent * max_Word_Horz_Hist
		#####fileWordHorzHist.write("\n Header limit (50 percent of max): %d " % (header_limit))

		header_width = 1
		#max row is itself of width 1

		#counting header width in forward/below direction
		for i in range(indexOfMax_Word_Horz_Hist+1, len(list_Word_Hor_Hist)):
			if (list_Word_Hor_Hist[i] > header_limit):
				header_width += 1
			else:
				break

		#counting header width in backward/above direction
		#from just before max to 0th or first row, subtracting by 1 (till -1)
		header_start_point = indexOfMax_Word_Horz_Hist
		for i in range(indexOfMax_Word_Horz_Hist-1, -1, -1):
			if (list_Word_Hor_Hist[i] > header_limit):
				header_width += 1
				header_start_point = i
			else:
				break

		#####fileWordHorzHist.write("\n Header width: %d " % (header_width))
		#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, HS: Header Start, hw = header width, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
		#List_Word_Split_Details.append(Dict)
		word['HS'] = BWy + header_start_point
		word['hw'] = header_width
		wordCount += 1
		#print wordCount
	#***************************************  for loop for each word ends here  ***************************************
	
	#####fileWordHorzHist.close()
	print "split upper: "
	print wordCount

	return List_Word_Details










def SplitWordLower(img, thresh_No_DE, List_Word_Split_Details_Upper, wordSplitTMBLowerThreshold, wordSplitTMBLowerHorHistThreshold):

	List_Word_Split_Details_Lower = []

	#####fileTest = open('charsInWordSpitLower.txt','w')
	#####fileTest1 = open('charsInWordSplitFinal.txt','w')
	
	#fileExtractChar = open('extractChar.txt','w')
	wordCount = 0

	
	for word in List_Word_Split_Details_Upper:

		#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, HS: Header Start, hw = header width, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
		

		ListCharsInWord = getCharsOfWord(word, thresh_No_DE)
		#Dict = {'BCx': BCx, 'BCy': BCy, 'ECx': ECx, 'ECy': ECy}
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate
		#####fileTest.write("\n\nLine no.: %d,  Word no. %d......... charCount: %d\n" % (word['lineNo'], word['wordNo'], len(ListCharsInWord)))
		charCount = 0
		sumCharLength = 0
		if(len(ListCharsInWord) != 0):
			#removing words with zero characters
			for char in ListCharsInWord:
				char = cleanChar(char, thresh_No_DE)
				char['length'] = char['ECy'] - char['BCy'] + 1
				#fileTest.write("\nChar: %d, length: %d, ybegin: %d, yend:%d" % (charCount, char['length'], char['BCy'], char['ECy']))
				#####fileTest.write("\nChar: %d, length: %d" % (charCount, char['length']))
				sumCharLength += char['length']
				charCount += 1
			meanCharLength = sumCharLength / charCount
			#####fileTest.write("\nmeanCharLength: %d" % (meanCharLength))
			maxCharLength = max(char['length'] for char in ListCharsInWord)
			#####fileTest.write("\nmaxCharLength: %d" % (maxCharLength))

			lower_modifier_threshold = wordSplitTMBLowerThreshold*meanCharLength
			if(maxCharLength - meanCharLength <= lower_modifier_threshold):
				word['LRS'] = -1
				#LRS : Lower Region Start = -1 means there is no lower region
			else:
				no_of_chars_with_lower_modifier = 0
				list_char_length = []
				for char in ListCharsInWord:
					list_char_length.append(char['length'])
					if(char['length'] > meanCharLength + lower_modifier_threshold):
						no_of_chars_with_lower_modifier += 1
				#####fileTest1.write("\n\nLine no.: %d,  Word no. %d, headerwidth: %d.........\n" % (word['lineNo'], word['wordNo'], word['hw']))
				#LRS = getLowerRegionOfWord(word, thresh_No_DE, wordSplitTMBLowerHorHistThreshold)
				#LRS = word['BWy'] + int(round(meanCharLength))
				meanCharLength = int(round(meanCharLength))
				#list_Word_Hor_Hist = wordHorHist(word, thresh_No_DE)
				#index_of_max_in_lower_region = list_Word_Hor_Hist.index(max(list_Word_Hor_Hist[meanCharLength:]))
				#real_index_of_max_in_lower_region = word['HS'] + index_of_max_in_lower_region

				#distance_of_max_from_lower_end = word['EWy'] - real_index_of_max_in_lower_region
				#LRS = real_index_of_max_in_lower_region - distance_of_max_from_lower_end

				max_length_of_no_lower_region_character = sorted(list_char_length)[-1 * (no_of_chars_with_lower_modifier + 1)]
				#LRS = word['HS'] + meanCharLength
				LRS = word['HS'] + max_length_of_no_lower_region_character
				word['LRS'] = LRS

				#####fileTest1.write("\nGapStart: %d"%(LRS))
			List_Word_Split_Details_Lower.append(word)
			#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
			#ECy : End Char Y-coordinate, HS: Header Start, LRS: Lower Region Start, 
			#lineNo: Line Number, wordNo: Word Number, charNo: Char Number
		
			wordCount += 1
			#print wordCount
	#***************************************  for loop for each word ends here  ***************************************
	
	#####fileTest.close()
	print "split lower: "
	print wordCount

	return List_Word_Split_Details_Lower










def SplitWordCharHorHist(img, thresh_No_DE, List_Word_Split_Details_Upper, wordSplitTMBLowerThreshold, wordSplitTMBLowerHorHistThreshold):

	#List_Word_Split_Details_Lower = []

	graphForWords = [[2,1], [4,10], [4,11]]

	fileTest = open('WordCharHorHist.txt','w')
	#pp = PdfPages('graphs.pdf')
	####for graph printing
	####pp = PdfPages('test2_graphs.pdf')
	wordCount = 0
	
	for word in List_Word_Split_Details_Upper:

		#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, HS: Header Start, hw = header width, lineNo: Line Number, 
		#wordNo: Word Number, charNo: Char Number
		#fileTest.write("\n\n\nwordNo: %d........." % (wordCount))
		fileTest.write("\n\nLine no.: %d,  Word no. %d.........\n" % (word['lineNo'], word['wordNo']))
		list_Word_Hor_Hist = wordHorHist(word, thresh_No_DE)
		


		ListCharsInWord = getCharsOfWord(word, thresh_No_DE)
		#Dict = {'BCx': BCx, 'BCy': BCy, 'ECx': ECx, 'ECy': ECy}
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate
		list_List_Char_Hor_Hist = []
		for char in ListCharsInWord:
			list_Char_Hor_Hist = charHorHist(char, thresh_No_DE)
			list_List_Char_Hor_Hist.append(list_Char_Hor_Hist)
		
		for i in range(0, len(list_Word_Hor_Hist)):
			strWrite = "\nrowNo: " + str(i) + " = " + str(list_Word_Hor_Hist[i]) + "    "
			for char_hist in list_List_Char_Hor_Hist:
				strWrite += " " + str(char_hist[i])
			fileTest.write(strWrite)

		fileTest.write("\n\nLine no.: %d,  Word no. %d......... charCount: %d\n" % (word['lineNo'], word['wordNo'], len(ListCharsInWord)))
		
		tmp_list = list_Word_Hor_Hist[::-1]
		#for reversing so that histogram earlier top was index 0, now bottom row of word is index 0
		####plt.plot(tmp_list, list(xrange(len(tmp_list))))
		###plt.title("lineNo: " + str(word['lineNo']) + ", wordNo: " + str(word['wordNo']))
		#plt.axis([0, 6, 0, 20])
		#plt.savefig("graph.png")
		####for char_hist in list_List_Char_Hor_Hist:
			####tmp_char_hist = char_hist[::-1]
			####plt.plot(tmp_char_hist, list(xrange(len(tmp_char_hist))))
		####pp.savefig()
		####plt.clf()
		#plt.show()
		
		wordCount += 1
		#print wordCount
	#***************************************  for loop for each word ends here  ***************************************
	#pp.close()
	fileTest.close()
	print "split lower: "
	print wordCount

	#return List_Word_Split_Details_Lower









def ExtractRegionTMB(List_Word_Split_Details_Lower, top_region_length_limit):

	List_Word_Split_Region = []
	count =0

	for word in List_Word_Split_Details_Lower:
		#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
		#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
		#ECy : End Char Y-coordinate, HS: Header Start, LRS: Lower Region Start, 
		#lineNo: Line Number, wordNo: Word Number, charNo: Char Number

		#Upper Region
		if(word['HS'] - word['BWy'] > top_region_length_limit):
			Dict1 = {'region': 1, 'hw': 1, 'BWx': word['BWx'], 'BWy' : word['BWy'], 'EWx': word['EWx'], 'EWy': word['HS']-1, 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
			#Dict1 = {'region': 1, 'hw': word['hw'], 'BWx': word['BWx'], 'BWy' : word['BWy'], 'EWx': word['EWx'], 'EWy': word['HS']-1, 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
			List_Word_Split_Region.append(Dict1)
			count += 1 
			#cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['HS']-1), (0,255,0), 1 )
		
		#If there is Lower Region
		if(word['LRS'] != -1):
			#Middle Region
			Dict2 = {'region': 2, 'hw': word['hw'], 'BWx': word['BWx'], 'BWy' : word['HS'], 'EWx': word['EWx'], 'EWy': word['LRS']-1, 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
			List_Word_Split_Region.append(Dict2)
			count += 1 
			#cv2.rectangle( img, (word['BWx'], word['HS']), (word['EWx'], word['LRS']-1), (255,0,0), 1 )
			
			#Lower Region
			Dict3 = {'region': 3, 'hw': 0, 'BWx': word['BWx'], 'BWy' : word['LRS'], 'EWx': word['EWx'], 'EWy': word['EWy'], 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
			List_Word_Split_Region.append(Dict3) 
			count += 1
			#cv2.rectangle( img, (word['BWx'], word['LRS']), (word['EWx'], word['EWy']), (0,0,255), 1 )
		
		#If there is No Lower Region
		else:
			Dict2 = {'region': 2, 'hw': word['hw'], 'BWx': word['BWx'], 'BWy' : word['HS'], 'EWx': word['EWx'], 'EWy': word['EWy'], 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
			List_Word_Split_Region.append(Dict2)
			count += 1
			#cv2.rectangle( img, (word['BWx'], word['HS']), (word['EWx'], word['EWy']), (255,0,0), 1 )
	print "split region"
	print count
	return List_Word_Split_Region










def getCharsOfWord(word, thresh_No_DE):
	#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, HS: Header Start, hw = header width, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
	
	BWx = word['BWx']
	BWy = word['HS']
	#only from start of header line, no upper region of a word
	EWx = word['EWx']
	EWy = word['EWy']
	header_width = word['hw']

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
		col_sum = 0

	length_col_sum = len(list_col_sum)
	ListCharsInWord = []

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
			#if width(no. of columns) of character is of atleast one stroke i.e. header width then only consider it as a char
			if(len(list_char) > header_width):
				BCx = BWx + list_char[0]
				BCy = BWy
				ECx = BWx + list_char[-1]
				ECy = EWy
				Dict = {'BCx': BCx, 'BCy': BCy, 'ECx': ECx, 'ECy': ECy}
				ListCharsInWord.append(Dict)

				charCount += 1

			i += len(list_char)

		else:
			i += 1
	return ListCharsInWord










def charHorHist(char, thresh_No_DE):

	BCx = char['BCx']
	BCy = char['BCy']
	ECx = char['ECx']
	ECy = char['ECy']

	row_sum = 0
	#header_width = 1
	list_Char_Hor_Hist = []
	for y in range(BCy, ECy+1):
		for x in range(BCx, ECx+1):
			pixel = thresh_No_DE[y,x]

			if(pixel==255):
				row_sum += 1

		list_Char_Hor_Hist.append(row_sum)
		row_sum = 0

	return list_Char_Hor_Hist










def cleanChar(char, thresh_No_DE):

	BCx = char['BCx']
	BCy = char['BCy']
	ECx = char['ECx']
	ECy = char['ECy']

	while(rowSum(thresh_No_DE, BCy, BCx, ECx) == 0):
		BCy += 1
	char['BCy'] = BCy

	while(rowSum(thresh_No_DE, ECy, BCx, ECx) == 0):
		ECy -= 1
	char['ECy'] = ECy

	return char










def rowSum(thresh_No_DE, y, BCx, ECx):
	rowSum = 0
	for x in range(BCx, ECx+1):
		pixel = thresh_No_DE[y,x]
		if(pixel==255):
			rowSum += 1
	return rowSum










def wordHorHist(word, thresh_No_DE):

	BWx = word['BWx']
	#BWy = word['BWy']
	BWy = word['HS']
	EWx = word['EWx']
	EWy = word['EWy']

	row_sum = 0
	#header_width = 1
	list_Word_Hor_Hist = []
	for y in range(BWy, EWy+1):
		for x in range(BWx, EWx+1):
			pixel = thresh_No_DE[y,x]

			if(pixel==255):
				row_sum += 1

		list_Word_Hor_Hist.append(row_sum)
		row_sum = 0

	return list_Word_Hor_Hist










def getLowerRegionOfWord(word, thresh_No_DE, wordSplitTMBLowerHorHistThreshold):

	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, HS: Header Start, hw = header width, lineNo: Line Number, wordNo: Word Number, charNo: Char Number
	
	

	list_Word_Hor_Hist = wordHorHist(word, thresh_No_DE)
	thresh = word['hw'] * wordSplitTMBLowerHorHistThreshold
	#wordSplitTMBLowerHorHistThreshold = 3
	listGapStart = []
	
	count = 0
	for i in range(len(list_Word_Hor_Hist)-1, 0, -1):
		if(count ==2):
			break
		if(list_Word_Hor_Hist[i-1] - list_Word_Hor_Hist[i] >= word['hw']):
			gapStart = i
			count +=1

	#LRS = word['BWy'] + listGapStart[-2]
	LRS = word['BWy'] + gapStart
	return LRS




