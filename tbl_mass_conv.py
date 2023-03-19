
import base64
import codecs
import os

from tkinter import filedialog as fd

class TBL:

    def __int__(self):
        self.dirPath = ''
        self.name = ''
        self.data = False

    def tblRead(self):

        with open(f'{self.dirPath}{self.name}.tbl', 'rb+') as inFile:

            inFile.seek(2)
            text = []
            headCount = inFile.read(4)
            headCount = int.from_bytes(headCount, byteorder = 'little')

            # if headCount != len(self.headString):
            #     print('Warning! Need more heads!')
            #     return

            h = []
            hs = []

            for hd in range(headCount):

                headString = b''

                while True:
                    char = inFile.read(1)
                    if char != b'\x00':
                        headString += char
                    else: break

                hs.append(str(headString)[2:-1])
                long = int.from_bytes(inFile.read(4), byteorder = 'little')
                h.append(long)

            for j in range(len(h)):
                head = hs[j]

                for i in range(h[j]):
                    inFile.seek(len(head) + 1, 1)
                    strSize = int.from_bytes(inFile.read(2), byteorder = 'little') - 3
                    strNum = int.from_bytes(inFile.read(2), byteorder = 'little')
                    string = inFile.read(strSize) if strSize > 0 else b''
                    inFile.seek(1, 1)
                    print(head, strNum, string)
                    text.append(f'{head}\t{strNum}\t{str(string)[2:-1]}\n')

        with open(f'{self.dirPath}{self.name}.txt', 'w') as outFile:
            outFile.writelines(text)

    def tblWrite(self):

        text = []

        with open(f'{self.dirPath}{self.name}.txt', 'r+') as inFile:
            text.append(inFile.readlines())

        with open(f'{self.dirPath}{self.name}.tbl', 'wb+') as outFile:

            count = len(text)
            outFile.write(count.to_bytes(6, byteorder = 'little'))

            for i in range(count):
                outFile.write(b'\x00')
                outFile.write(len(text[i]).to_bytes(2, byteorder = 'little'))
                outFile.write(i.to_bytes(2, byteorder = 'little'))
                outFile.write(base64.b64encode(text[i]))
                outFile.write(codecs.encode(self.headString, 'UTF-16-le'))
                outFile.write(b'\x00')


filetypes = (('TBL Files', '*.tbl'), ('TXT Files', '*.txt'), ('All files', '*.*'))
filename = fd.askopenfilename(title = 'Выберите XLSX файл', filetypes = filetypes)


conv = TBL()

conv.dirPath = os.path.dirname(filename) + '/'
conv.name = os.path.basename(filename).split('.')[0]

conv.tblRead()
