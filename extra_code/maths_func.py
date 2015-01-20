import heapq



def MinGreatKey(List, key):

	a = 1000
	for item in List:
		if(item > 2 and item < a):
			a=item
	if (a==1000):
		a = 3
	return a



def nth_smallest(iter, n):
	return heapq.nsmallest(n, iter)[-1]



def wordSpecificLimit(List, minDifference):
	diff = 0
	i = 1

	while(i < len(List)):
	#while(True):
		
		tmp1 = nth_smallest(List, i)
		tmp2 = nth_smallest(List, i+1)
		diff =  tmp2 - tmp1
		#print("tmp1 tmp2 diff")
		#print tmp1, tmp2, diff
		i += 1
		if((diff >= minDifference) and (tmp1 > 3)):
			break

	return tmp1


'''
def localMinimum(List):

	size = len(List)
	for i in range(1, size):

'''

def greaterLeft(List, index):
	tmp_val = -1
	tmp_idx = index
	value = List[index]
	while(tmp_idx >= 0 and List[tmp_idx] > value):
		#print tmp_idx
		tmp_idx -= 1

	return tmp_idx




#ls = [0, 1, 4, 5, 8, 10, 10, 10, 12, 12, 9, 6, 4, 3, 5, 8, 11, 18, 18, 18, 5, 3, 3, 4, 5, 10, 13, 14, 14, 14, 12, 10, 8, 6, 6, 10, 18, 18, 18, 5, 4, 3, 3, 8, 10, 13, 11, 11, 11, 11, 10, 10, 14, 17, 19, 19, 19, 5, 4, 4, 5, 11, 11, 15, 2, 0]
#x=15
#print ls[x]
#print greaterLeft(ls, x)
#listwa = [0, 1, 4, 5, 8, 10, 10, 10, 12, 12, 9,6,4,3,5,8,11,18,18,18,5,3,3,4,5,10,13,14,14,14,12]
#print wordSpecificLimit(ls, 3)
