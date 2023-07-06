import os
from pprint import pprint
from tkinter import filedialog as fd


def dds_save(x, y, palette, name, data):

    with open(f'{name}.dds', 'wb') as dds_file:
        dds_file.write(b'\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x0A\x00')
        dds_file.write(x.to_bytes(4, byteorder='little'))
        dds_file.write(y.to_bytes(4, byteorder='little'))
        dds_file.write(b'\x70\x55\x05\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00')
        dds_file.write(palette)
        dds_file.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        dds_file.write(data)


def png_save(x, y, palette, name, data):
    print('TODO: добавить поддержку PNG')


def open_file(phyre_file=''):
    if phyre_file == '':
        filetypes = (('Phyre files', '*.phyre'), ('All files', '*.*'))
        phyre_file = fd.askopenfilename(title='Выберите Phyre файл',
                                        filetypes=filetypes)

    if phyre_file == '':
        input('Файл не выбран!')
        return

    full_name = phyre_file.split('.')
    file_type = full_name[1].split('_')[0]
    name = full_name[0]

    if file_type == 'dds':
        ft = b'dds\x00'
        head_size = 42
    elif file_type == 'png':
        ft = b'png\x00'
        head_size = 43
    else:
        input('Неподдреживемый тип файла!')
        return

    with open(phyre_file, 'rb') as phyre:

        phyre.seek(4)
        size = int.from_bytes(phyre.read(4), byteorder='little')
        metaSize = int.from_bytes(phyre.read(4), byteorder='little')
        platform = phyre.read(4).decode('utf-8')

        if platform != '1XNG':
            input('Неподдерживаемая платформа\n'
                  'Выберите файл для Switch версии игры!')
            return

        phyre.seek(72, 1)
        baseHeaderSize = int.from_bytes(phyre.read(4), byteorder='little')
        varsCount = int.from_bytes(phyre.read(4), byteorder='little')
        dirsCount = int.from_bytes(phyre.read(4), byteorder='little')
        paramsCount = int.from_bytes(phyre.read(4), byteorder='little')
        tableSize = int.from_bytes(phyre.read(4), byteorder='little')
        stringTableOffset = size + metaSize - tableSize
        phyre.seek(8, 1)
        startTableDataStart = phyre.tell()

        phyre.seek(stringTableOffset)
        table = phyre.read(tableSize)
        stringTable = [t.decode('utf-8') for t in table.split(b'\x00')][:-1]

        with open('temp.dat', 'wb') as temp_file:
            temp_file.write(table)

        phyre.seek(startTableDataStart)

        paramsList = {}

        def getName(o):

            with open('temp.dat', 'rb') as temp2:
                temp2.seek(o)
                return temp2.read().split(b'\x00')[0].decode('utf-8')

        for c in range(varsCount):
            offset = int.from_bytes(phyre.read(4), byteorder='little')
            paramsList[getName(offset)] = {'offset': offset}

        for d in range(varsCount, varsCount + dirsCount):
            parentDirId = int.from_bytes(phyre.read(4), byteorder='little')
            data = phyre.read(4)
            offset = int.from_bytes(phyre.read(4), byteorder='little')
            magic = [phyre.read(4) for _ in range(6)]
            paramsList[getName(offset)] = {'parentDirId': parentDirId,
                                           'data': data,
                                           'offset': offset,
                                           'magic': magic}

        for e in range(dirsCount + varsCount, len(stringTable) + 6):
            offset = int.from_bytes(phyre.read(4), byteorder='little')
            tp = int.from_bytes(phyre.read(4), byteorder='little')
            magic = [phyre.read(4) for _ in range(4)]
            paramsList[getName(offset)] = {'offset': offset,
                                           'type': tp,
                                           'magic': magic}

        pprint(paramsList)
        phyre.seek(0)
        data = phyre.read().split(b'\x00PTexture2D\x00')
        image = data[-1]

    size = data[-2].split(ft)[-1]
    p = image[:5]
    image_data = image[head_size:]
    start = 0 if len(size) % 2 == 0 else 1
    x_pos = int.from_bytes(paramsList['m_width']['magic'][0], byteorder='little') + start
    y_pos = int.from_bytes(paramsList['m_height']['magic'][0], byteorder='little') + start
    x = int.from_bytes(size[x_pos:x_pos + 4], byteorder='little')
    y = int.from_bytes(size[y_pos:y_pos + 4], byteorder='little')

    with open(f'{name}.bin', 'wb') as head_file:

        for d in range(len(data) - 1):
            head_file.write(data[d])
            head_file.write(b'\x00PTexture2D\x00')

    if file_type == 'dds':
        dds_save(x, y, p, name, image_data)

        # if x != y:
        #     dds_save(y, x, p, f'{name}_reverse', image_data)

    elif file_type == 'png':
        png_save(x, y, p, name, image_data)


if __name__ == "__main__":
    open_file()
    # open_file('C:\\Users\\I\\Desktop\\out\\0a19jim0.dds.phyre')

    # path = 'C:\\Users\\I\\Desktop\\out\\'
    #
    # for root, dirs, files in os.walk(path):
    #
    #     for filename in files:
    #
    #         if 'dds' in filename and 'phyre' in filename:
    #             print(path + filename)
    #             open_file(path + filename)
