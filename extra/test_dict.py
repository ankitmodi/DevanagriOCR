
mylist =[]
dict1 = {'id': 'a', 'Bx': 1, 'By': 2, 'Ex': 3, 'Ey': 4}
mylist.append(dict1)
dict1 = {'id': 'b', 'Bx': 11, 'By': 12, 'Ex': 13, 'Ey': 14};
mylist.append(dict1)

mylist.append({'id': 'c', 'Bx': 1, 'By': 2, 'Ex': 3, 'Ey': 4})
for item in mylist:
	print item['id']