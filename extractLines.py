import cv2
import numpy as np

def ExtractLines(img, thresh, pixel_Limit_Line_Extraction):

	#height, width, depth = img.shape
	max_y, max_x, depth = img.shape
	#print max_x, max_y

	#fileRowSum = open('hh_rowSum_without_DE.txt','w')
	#####fileRowSum = open('rowSum_No_DE.txt','w')

	pixel_Limit_Line_Extraction = 3
	row_sum = 0
	list_row_sum = []

	#Go through all the pixels in each row i.e. y. For each row, if it contains a pixel==255 then add 1 to that row's pixel count
	for y in range(0,max_y):
		for x in range(0, max_x):
			pixel = thresh[y,x]

			if(pixel==255):
				row_sum += 1

		list_row_sum.append(row_sum)
		#print no. of pixels==255 in each row
		#####fileRowSum.write("row: %d = %d\n" % (y, list_row_sum[y]))
		row_sum = 0

	#####fileRowSum.close()

	
	#Extracting lines
	List_Line_Details = []

	
	length_row_sum = len(list_row_sum)

	i = 0
	while(i < length_row_sum):
		if( list_row_sum[i] > pixel_Limit_Line_Extraction):
			list_line = []
			for j in range(i, length_row_sum):
				if( list_row_sum[j] > pixel_Limit_Line_Extraction):
					list_line.append(j)
				else:
					break

			Dict = {'LB': list_line[0], 'LE': list_line[-1]}
			#'LB': Line Begin 'LE': Line End
			List_Line_Details.append(Dict)

			i += len(list_line)
			
		else:
			i += 1


	print "No. of lines: "
	print len(List_Line_Details)
	return List_Line_Details