
import os
import tkinter as tk
from tkinter import filedialog
import ctypes

root = tk.Tk()
root.withdraw()
file_path = filedialog.askdirectory()

name = file_path.split('/')[-1]
folder = file_path[0:-len(name)]
fileList = os.listdir(file_path)
list1 = b''

for n in fileList: list1 += n.split('.')[1].encode('utf-8') + b'\x00'

blockOff = 33 + len(name)
contOff = len(fileList)
size = contOff * 4
endBlock = blockOff + size
block2Strt = blockOff + (contOff * 6)
strtData = block2Strt + len(list1)

with open(file_path + '_new.dat', 'wb') as f: 
	f.write(b'\x20\x00\x00\x00\x20\x00\x00\x00')
	f.write(blockOff.to_bytes(4, byteorder='little'))
	f.write(size.to_bytes(4, byteorder='little'))
	f.write(endBlock.to_bytes(4, byteorder='little'))
	f.write(contOff.to_bytes(4, byteorder='little'))
	f.write(strtData.to_bytes(4, byteorder='little'))
	f.write(b'\x00\xef\xcd\xab')
	f.write(name.encode('utf-8') + b'\x00')
	strtData += 1
	f.write(strtData.to_bytes(4, byteorder='little'))
	for i in range(len(fileList) - 1):
		strtData += os.path.getsize(file_path + '/' + fileList[i])
		f.write(strtData.to_bytes(4, byteorder='little'))

	f.write(block2Strt.to_bytes(2, byteorder='little'))
	for j in range(len(fileList) - 1):
		block2Strt += len(fileList[j]) - 9
		f.write(block2Strt.to_bytes(2, byteorder='little'))

	f.write(list1 + b'\x00')

	for file in fileList:
		with open(file_path + '/' + file, 'rb') as readF:
			readData = readF.read()
		f.write(readData)

ctypes.windll.user32.MessageBoxW(0, folder, name)
