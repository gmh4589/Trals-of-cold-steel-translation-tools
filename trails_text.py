#патчит файлы, добавляя в них метки для оффсетов

import re
import os.path

f_ar = ['system.dat', 't0000b.dat', 't0000c.dat', 'a0000.dat', 'a0001.dat', 'a0002.dat', 'a0003.dat', 'a0004.dat', 'a0005.dat', 'a0006.dat', 'a0007.dat', 'a0008.dat', 'a0009.dat', 'a0010.dat', 'a0011.dat', 'a0100.dat', 'a0101.dat', 'a0102.dat', 'a0103.dat', 'a0104.dat', 'a0120.dat', 'a0121.dat', 'a0122.dat', 'a0123.dat', 'a0124.dat', 'a0125.dat', 'a0126.dat', 'a0127.dat', 'a0193.dat', 'a0194.dat', 'a0195.dat', 'a0196.dat', 'a0197.dat', 'a0198.dat', 'a0199.dat', 'a0200.dat', 'a0201.dat', 'a0202.dat', 'a0203.dat', 'a0204.dat', 'a0205.dat', 'a0206.dat', 'a0500.dat', 'a1301.dat', 'a1400.dat', 'a1500.dat', 'a1600.dat', 'a1700.dat', 'a1701.dat', 'a1900.dat', 'a1901.dat', 'a1902.dat', 'a2000.dat', 'a2002.dat', 'a2003.dat', 'a2005.dat', 'a2006.dat', 'a2009.dat', 'a3000.dat', 'a4600.dat', 'a9999.dat', 'c0000.dat', 'c0010.dat', 'c0020.dat', 'c0100.dat', 'c0110.dat', 'c0120.dat', 'c0130.dat', 'c0140.dat', 'c0150.dat', 'c0200.dat', 'c0210.dat', 'c0220.dat', 'c0230.dat', 'c0300.dat', 'c0310.dat', 'c0330.dat', 'c0350.dat', 'c0360.dat', 'c0400.dat', 'c0410.dat', 'c0430.dat', 'c0440.dat', 'c0450.dat', 'c0460.dat', 'c0500.dat', 'c0600.dat', 'c0610.dat', 'c0620.dat', 'c0700.dat', 'c0710.dat', 'c0800.dat', 'c0910.dat', 'c0930.dat', 'c0950.dat', 'c0960.dat', 'debug.dat', 'e0030.dat', 'e0050.dat', 'e2000.dat', 'e2001.dat', 'e5010.dat', 'e5011.dat', 'e5012.dat', 'e5210.dat', 'e5310.dat', 'e5410.dat', 'e5510.dat', 'e5610.dat', 'e5630.dat', 'e6410.dat', 'e7010.dat', 'e8410.dat', 'e9000.dat', 'e9010.dat', 'e9100.dat', 'e9101.dat', 'm0010.dat', 'm0020.dat', 'm0030.dat', 'm0040.dat', 'm0500.dat', 'm0510.dat', 'm0520.dat', 'm0530.dat', 'm1000.dat', 'm1001.dat', 'm1010.dat', 'm1020.dat', 'm1030.dat', 'm1040.dat', 'm1050.dat', 'm1060.dat', 'm1070.dat', 'm1200.dat', 'm1210.dat', 'm1220.dat', 'm1230.dat', 'm1240.dat', 'm1260.dat', 'm1500.dat', 'm1540.dat', 'm2000.dat', 'm2001.dat', 'm2005.dat', 'm2020.dat', 'm2021.dat', 'm2022.dat', 'm2100.dat', 'm2110.dat', 'm2120.dat', 'm2130.dat', 'm2500.dat', 'm2501.dat', 'm2502.dat', 'm2503.dat', 'm2504.dat', 'm2505.dat', 'm2510.dat', 'm2511.dat', 'm2512.dat', 'm2520.dat', 'm2521.dat', 'm2522.dat', 'm2530.dat', 'm2531.dat', 'm2532.dat', 'm2533.dat', 'm2540.dat', 'm2541.dat', 'm2542.dat', 'm2543.dat', 'm2550.dat', 'm2551.dat', 'm2552.dat', 'm2553.dat', 'm2560.dat', 'm2561.dat', 'm2562.dat', 'm2563.dat', 'm3000.dat', 'm3001.dat', 'm3002.dat', 'm3003.dat', 'm3004.dat', 'm3007.dat', 'm3008.dat', 'm3050.dat', 'r0000.dat', 'r0010.dat', 'r0020.dat', 'r0030.dat', 'r0100.dat', 'r0130.dat', 'r0200.dat', 'r0210.dat', 'r0220.dat', 'r0300.dat', 'r0310.dat', 'r0400.dat', 'r0410.dat', 'r0420.dat', 'r0430.dat', 'r0600.dat', 'r0601.dat', 'r0610.dat', 'r0800.dat', 'r0801.dat', 'r0810.dat', 't0000.dat', 't0010.dat', 't0020.dat', 't0030.dat', 't0031.dat', 't0032.dat', 't0050.dat', 't0060.dat', 't0070.dat', 't0080.dat', 't0090.dat', 't0100.dat', 't0200.dat', 't0201.dat', 't0210.dat', 't1000.dat', 't1010.dat', 't1020.dat', 't1030.dat', 't1040.dat', 't1050.dat', 't1060.dat', 't1070.dat', 't1080.dat', 't1090.dat', 't1110.dat', 't1120.dat', 't1150.dat', 't1160.dat', 't1500.dat', 't1510.dat', 't1530.dat', 't1540.dat', 't1550.dat', 't1560.dat', 't1570.dat', 't1600.dat', 't1610.dat', 't2000.dat', 't2010.dat', 't2020.dat', 't2100.dat', 't2110.dat', 't2120.dat', 't2130.dat', 't2200.dat', 't2210.dat', 't2220.dat', 't2300.dat', 't2310.dat', 't2320.dat', 't2330.dat', 't2340.dat', 't3000.dat', 't3010.dat', 't3020.dat', 't3030.dat', 't3040.dat', 't3050.dat', 't3060.dat', 't3070.dat', 't3090.dat', 't3100.dat', 't3500.dat', 't3510.dat', 't3520.dat', 't3530.dat', 't3550.dat', 't3560.dat', 't3570.dat', 't3580.dat', 't3590.dat', 't3600.dat', 't3610.dat', 't3620.dat', 't3630.dat', 't3710.dat', 't3720.dat', 't3730.dat', 't3740.dat', 't3750.dat', 't3780.dat', 't3790.dat', 't4500.dat', 't4510.dat', 't4520.dat', 't4530.dat', 't4540.dat', 't4550.dat', 't4600.dat', 't4610.dat', 't4700.dat', 't4810.dat', 't4830.dat', 't5000.dat', 't5010.dat', 't5500.dat', 't5510.dat', 't5520.dat', 't5530.dat', 't5610.dat', 't5620.dat', 't5630.dat', 't5640.dat', 't5650.dat', 't5660.dat', 't5700.dat', 'book00.dat', 'book01.dat', 'book02.dat', 'book03.dat']

for b in range(len(f_ar)):
	#print (f_ar[b] + ' start!')
	name = 'in/' + f_ar[b]
	fp = open(name, 'rb+')
	new = 'out/' + f_ar[b]
	fn = open(new, 'wb+')

	fp.seek(20, 0)
	a = fp.read(4)
	a = int.from_bytes(a, byteorder='little')
	#print(a)
	if len(f_ar[b]) == 10:
		z = 39
	else:
		z = 38
	fp.seek(z, 0)

	OffsetList = []

	for i in range(a):
		x = fp.read(4)
		x = int.from_bytes(x, byteorder='little')
		OffsetList.append(x)
	#print (OffsetList)
	
	Blocks = []

	for j in range(a):
		fp.seek(OffsetList[j])
		if (j+1) == a:
			block = fp.read()
		else:
			d = OffsetList[j+1] - OffsetList[j]
			block = fp.read(d)
		Blocks.append(block)
		# print(block)
		
	fp.seek(24, 0)
	l = fp.read(4)
	l = int.from_bytes(l, byteorder='little')
	fp.seek(0)
	head = fp.read(l)
	fn.write(head)
	xmark = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'

	for k in range(a):
		fn.write(xmark)
		fn.write(Blocks[k])
	
	print (f_ar[b] + ' done!')
		

input('Press any key')