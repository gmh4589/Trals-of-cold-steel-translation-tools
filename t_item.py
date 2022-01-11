
import re
import os.path
import base64
import codecs

name = 't_item.tbl'

file = open(name, 'rb+')
new = 't_item.csv'
fn = open(new, 'w+')

count = file.read(2)
count = int.from_bytes(count, byteorder='little')

data = file.read()
strings = data.split (b'item')

for i in range(count):
	if i > 0:
		n = int.from_bytes(strings[i][3:5], byteorder='little')
		# print(s)
		d = base64.b64encode(strings[i][6:60])
		# print(d)
		t = codecs.decode(strings[i][60:-2], 'UTF-16-le')
		fn.write (str(n) + '\t' + str(d) + '\t' + t + '\n')
		
input('Press any key')
