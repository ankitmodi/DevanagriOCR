import cv2
import numpy as np
from matplotlib import pyplot as plt

#Author of these imported file: Ankit Modi
import preprocess
import extractLines
import extractWords
import extractChars
#import histogram
import extractBoundaryRefine
import charDimension
import wordSplitTMB   # TMB: Top, Mid, Bottom
import wordVertHist

pixel_Limit_Line_Extraction = 0
pixel_Limit_Word_Extraction = 0
pixel_Limit_Char_Extraction = 4

# 90 percent : 0.1
header_Line_Percent = 0.50

top_region_length_limit = 2

wordSplitTMBLowerThreshold = 0.2
#0.3: 30%
wordSplitTMBLowerHorHistThreshold = 3
# 3 times

# Load the image
img = cv2.imread('zz_athva.jpg')
#img = cv2.imread('chandra.png')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



#**********************************Pre Processing***********************************************************************



#draw histogram
#hist_array = histogram.plotHist(img)

thresh, thresh_No_DE, thresh_color = preprocess.InitialPreprocess(img)



#******************************Line Segmentation***********************************************************************



List_Line_Details = extractLines.ExtractLines(img, thresh_No_DE, pixel_Limit_Line_Extraction)
#print len(list_Line_Begin), len(list_Line_End)

'''
#height, width, depth = img.shape
max_y, max_x, depth = img.shape
# LB: Line Begin           LE: Line End
for line in List_Line_Details:
	#cv2.line(thresh_color,(0,LB),(max_x,LB),(0,255,0),1)
	#line begin
	LB = line['LB']
	#line end
	LE = line['LE']
	cv2.line(img,(0,LB),(max_x,LB),(0,255,0),1)

	#cv2.line(thresh_color,(0,LE),(max_x,LE),(0,0,255),1)
	cv2.line(img,(0,LE),(max_x,LE),(0,0,255),1)

#cv2.imshow('Draw thresh',thresh_color)
#cv2.imwrite('zz_lines_thresh_color.jpg',thresh_color)
cv2.imshow('Lines',img)
cv2.imwrite('zz1_lines_img.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


#******************************Word Segmentation***********************************************************************



#WBx is Word Begin X-coordinate
#WBy is Word End Y-Coordinate


#Word boundary refining
List_Word_Details_Unrefined = extractWords.ExtractWords(img, thresh_No_DE, List_Line_Details, pixel_Limit_Word_Extraction)


'''
for word in List_Word_Details_Unrefined:
	#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
	#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number
	cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['EWy']), (255,0,0), 1 )
 	#print word['lineNo']

# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz2_words_img.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

List_Word_Details = extractBoundaryRefine.refineWord(img, thresh_No_DE, List_Word_Details_Unrefined)

'''
fileWordBoundary = open('WordBoundary.txt','w')

#for (x1, y1, x2, y2) in zip(beginWordX, beginWordY, endWordX, endWordY):
for word in List_Word_Details_Unrefined:

	#BWx: Begin Word X-coordinate, BWy: Begin Word Y-coordinate, EWx : End Word X-coordinate, 
	#EWy : End Word Y-coordinate, lineNo: Line Number, wordNo: Word Number
	cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['EWy']), (255,0,0), 1 )
	fileWordBoundary.write("(%d, %d)  (%d, %d)  lineNo: %d  wordNo: %d\n" % (word['BWx'], word['BWy'], word['EWx'], word['EWy'], word['lineNo'], word['wordNo']))

fileWordBoundary.close()

# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz3_words_refine_img.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''



#*****************************Split Word in three parts: Top, Mid and Bottom **************************
List_Word_Split_Details_Upper = wordSplitTMB.SplitWordUpper(img, thresh_No_DE, List_Word_Details, header_Line_Percent)

'''
for word in List_Word_Split_Details_Upper:
	#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, HS: Header Start,, hw = header width, lineNo: Line Number, 
	#wordNo: Word Number, charNo: Char Number
	if(word['HS'] - word['BWy'] > top_region_length_limit):
		cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['HS']-1), (0,0,255), 1 )
	cv2.rectangle( img, (word['BWx'], word['HS']), (word['EWx'], word['EWy']), (255,0,0), 1 )
	
# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz4_word_split_img.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


#wordVertHist.drawVertHist(List_Word_Split_Details_Upper, thresh_No_DE)

#*****************************Split Word in three parts: Top, Mid and Bottom **************************
List_Word_Split_Details_Lower = wordSplitTMB.SplitWordLower(img, thresh_No_DE, List_Word_Split_Details_Upper, wordSplitTMBLowerThreshold, wordSplitTMBLowerHorHistThreshold)


#*****************************Make Histograms **************************

#wordSplitTMB.SplitWordCharHorHist(img, thresh_No_DE, List_Word_Split_Details_Upper, wordSplitTMBLowerThreshold, wordSplitTMBLowerHorHistThreshold)

#***********************************************************************
'''
for word in List_Word_Split_Details_Lower:
	#Dict = {'BWx': BWx, 'BWy' : BWy, 'EWx': EWx, 'EWy': EWy, 'HS': BWy + header_start_point, 'lineNo': lineCount, 'wordNo': wordCount}
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, HS: Header Start, hw = header width, LRS: Lower Region Start, 
	#lineNo: Line Number, wordNo: Word Number, charNo: Char Number

	#Upper Region
	if(word['HS'] - word['BWy'] > top_region_length_limit):
		cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['HS']-1), (0,255,0), 1 )
	
	#If there is Lower Region
	if(word['LRS'] != -1):
		#Middle Region
		cv2.rectangle( img, (word['BWx'], word['HS']), (word['EWx'], word['LRS']-1), (255,0,0), 1 )
		#Lower Region
		cv2.rectangle( img, (word['BWx'], word['LRS']), (word['EWx'], word['EWy']), (0,0,255), 1 )
	
	#If there is No Lower Region
	else:
		cv2.rectangle( img, (word['BWx'], word['HS']), (word['EWx'], word['EWy']), (255,0,0), 1 )
	
# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz5_word_splitLower_img.jpg',img)
#cv2.imwrite('testResult.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''



#******************************Character Segmentation********************************************************************
List_Word_Split_Region = wordSplitTMB.ExtractRegionTMB(List_Word_Split_Details_Lower, top_region_length_limit)

#Dict1 = {'region': 1, 'hw': 0, 'BWx': word['BWx'], 'BWy' : word['BWy'], 'EWx': word['EWx'], 'EWy': word['HS']-1, 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
#Dict2 = {'region': 2, 'hw': word['hw'], 'BWx': word['BWx'], 'BWy' : word['HS'], 'EWx': word['EWx'], 'EWy': word['LRS']-1, 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}
#Dict3 = {'region': 3, 'hw': 0, 'BWx': word['BWx'], 'BWy' : word['LRS'], 'EWx': word['EWx'], 'EWy': word['EWy'], 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}

#if no lower region
#Dict2 = {'region': 2, 'hw': word['hw'], 'BWx': word['BWx'], 'BWy' : word['HS'], 'EWx': word['EWx'], 'EWy': word['EWy'], 'lineNo': word['lineNo'], 'wordNo': word['wordNo']}

'''
for word in List_Word_Split_Region:
	
	if(word['region'] == 1):
		cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['EWy']), (255,0,0), 1 )
	elif(word['region'] == 2):
		cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['EWy']), (0,0,255), 1 )
	else:
		cv2.rectangle( img, (word['BWx'], word['BWy']), (word['EWx'], word['EWy']), (0,255,0), 1 )
	
# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz6_word_split_region_img.jpg',img)
#cv2.imwrite('testResult.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''



#************************************Character Segmentation********************************************************************

List_Char_Details_Unrefined = extractChars.ExtractChars(img, thresh_No_DE, List_Word_Split_Region)


'''
for char in List_Char_Details_Unrefined:
	#Dict = {'BCx': BCx, 'BCy': BCy, 'ECx': ECx, 'ECy': ECy, 'lineNo': word['lineNo'], 'wordNo': word['wordNo'], 'region': word['region'], 'charNo': charCount, 'hw': header_width}
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, 
	#region: Top-Mid-Bot 1-2-3, charNo: Char Number, hw: header width(0 for Top-Bot)
	
	if(char['region']==1):			
		cv2.rectangle( img, (char['BCx'], char['BCy']), (char['ECx'], char['ECy']),(0,0,255),1)
	elif(char['region']==2):			
		cv2.rectangle( img, (char['BCx'], char['BCy']), (char['ECx'], char['ECy']),(255,0,0),1)
	else:			
		cv2.rectangle( img, (char['BCx'], char['BCy']), (char['ECx'], char['ECy']),(0,255,0),1)
	
# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz7_chars_img.jpg',img)
#cv2.imwrite('chandra_chars_img.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
'''
for i in (1,10):
	char = List_Char_Details_Unrefined[i]
'''



List_Char_Details_Refined = extractBoundaryRefine.refineChar(img, thresh_No_DE, List_Char_Details_Unrefined)



'''
fileCharBoundary = open('CharBoundary.txt','w')

for char in List_Char_Details:
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number, hw: header_width
	cv2.rectangle( img, (char['BCx'], char['BCy']), (char['ECx'], char['ECy']),(255,0,0),1)
	fileCharBoundary.write("(%d, %d)  (%d, %d)  lineNo: %d  wordNo: %d  charNo: %d\n" % (char['BCx'], char['BCy'], char['ECx'], char['ECy'], char['lineNo'], char['wordNo'], char['charNo']))

fileCharBoundary.close()

# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz1_chars_refine_img.jpg',img)
#cv2.imshow('res',thresh_color)
#cv2.imwrite('zz1_chars_thresh_color.jpg',thresh_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''



#******************************Character Width-Height  Calculation *************************************



List_Char_Details_WH, mean_width, mean_height = charDimension.calculateCharDimension(List_Char_Details_Refined)
#List_Char_Details_WH, mean_width, mean_height = charDimension.calculateCharDimension(List_Char_Details_Unrefined)
#with WH (width and height)
#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number, 
#width: Char Width, height: Char Height, hw: header_width

#print List_Char_Details_WH[0]



#********************************************Filter based on character width*****************************************


'''
width_limit_percent = 2
# 2: filter those greater than 200% of mean_width
List_Char_Details_FCW = extractChars.FilterCharWidth(thresh_No_DE, List_Char_Details_WH, mean_width, width_limit_percent)
#with FCW (Filter on Character Width)


fileCharBoundary = open('CharBoundarySplit.txt','w')

for char in List_Char_Details_FCW:
	#BCx: Begin Char X-coordinate, BCy: Begin Char Y-coordinate, ECx : End Char X-coordinate, 
	#ECy : End Char Y-coordinate, lineNo: Line Number, wordNo: Word Number, charNo: Char Number,
	#width: Char Width, height: Char Height, hw: header_width, 
	#splitNo: if not split then -1, else the split no in joint char

	fileCharBoundary.write("(%d, %d)  (%d, %d)  lineNo: %d  wordNo: %d  charNo: %d\n" % (char['BCx'], char['BCy'], char['ECx'], char['ECy'], char['lineNo'], char['wordNo'], char['charNo']))
	if(char['splitNo'] != -1):
		cv2.rectangle( img, (char['BCx'], char['BCy']), (char['ECx'], char['ECy']),(0,0,255),1)
	#else:
		#cv2.rectangle( img, (char['BCx'], char['BCy']), (char['ECx'], char['ECy']),(255,0,0),1)
		

fileCharBoundary.close()

# Finally show the image
cv2.imshow('img',img)
cv2.imwrite('zz1_chars_split_img.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''



#***************************************************************************************************************************
'''

# Find the contours
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

# For each contour, find the bounding rectangle and draw it
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.rectangle(thresh_color,(x,y),(x+w,y+h),(0,255,0),2)

# Finally show the image
cv2.imshow('img',img)
cv2.imshow('res',thresh_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

