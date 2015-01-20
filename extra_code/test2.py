import heapq

def nth_smallest(iter, n):
    return heapq.nsmallest(n, iter)[-1]


L=[1,2,5,3,0,5]
print nth_smallest(L, 0)
