# выводит список номеров строк в t_text.tbl

import re
import os.path

name = 't_text.tbl'

file = open(name, 'rb+')

b = 16

for i in range (0, 430):
	file.seek(b, 1)
	bb = file.read(2)
	b = int.from_bytes(bb, byteorder='little')
	cc = file.read(2)
	c = int.from_bytes(cc, byteorder='little')
	if (c != i):
		print(str(i) + ' ' + str(c))
	file.seek(12, 1)
	
input('Press any key')