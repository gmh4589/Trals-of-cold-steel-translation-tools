from os import path
from tkinter import filedialog as fd
from PIL import Image


def name_check(name):
    a = 0
    new_name = name

    while True:
        a += 1

        if path.exists(f'{new_name}.dds'):
            new_name += f'{name}_{a}'
        else:
            break

    return new_name


def dds_save(x, y, codec, name, data):

    with open(f'{name_check(name)}.dds', 'wb') as dds_file:
        dds_file.write(b'DDS\x20\x7C\x00\x00\x00\x07\x10\x0A\x00')
        dds_file.write(x.to_bytes(4, byteorder='little'))
        dds_file.write(y.to_bytes(4, byteorder='little'))
        dds_file.write(b'\x70\x55\x05\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00')
        dds_file.write(codec)
        dds_file.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        dds_file.write(data)


def bmp_save(x, y, codec, name, data):

    name = name_check(name)
    codec = codec.decode('utf-8')[:-1]

    Image.frombytes(codec, (y, x), data).save(f'{name}.bmp')


def phyre_save(name):

    ext = name.split('.')[-1]
    x, y = Image.open(name).size

    with open(name, 'rb') as image_file:
        image_file.seek(128 if ext == 'dds' else 150)
        image_data = image_file.read()

    with open(name.replace(ext, 'bin'), 'rb') as head_file:
        head_data = head_file.read()

    new_file = name + '_new.phyre' if 'bmp' not in name else name.replace('bmp', 'png') + '_new.phyre'

    with open(new_file, 'wb') as new_phyre:
        new_phyre.write(head_data)
        new_phyre.write(x.to_bytes(4, byteorder='little'))
        new_phyre.write(y.to_bytes(4, byteorder='little'))
        new_phyre.write(b'\x01\x00\x00\x00\x00\x50\x54\x65\x78\x74\x75\x72\x65\x32\x44\x00')
        new_phyre.write(b'DXT5' if ext == 'dds' else b'RGBA8')
        new_phyre.write(b'\x00\x08\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00')
        new_phyre.write(b'\x05' if ext == 'dds' else b'\x06')
        new_phyre.write(b'\x00\x00\x00\x0B\x00\x00\x00\x58\x02\x00\x01\x48\x04\x01\x48\x4E\x02\x08\x01\x00')
        new_phyre.write(image_data)


def open_file(phyre_file=''):

    if phyre_file == '':
        filetypes = (('Phyre files', '*.phyre; *.png; *.dds; *.bmp'), ('All files', '*.*'))
        phyre_file = fd.askopenfilename(title='Выберите Phyre файл',
                                        filetypes=filetypes)

    if phyre_file == '':
        input('Файл не выбран!')
        return

    if phyre_file.split('.')[-1] != 'phyre':
        phyre_save(phyre_file)
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

        # pprint(paramsList)
        phyre.seek(0)
        data = phyre.read().split(b'\x00PTexture2D\x00')
        image = data[-1]

    size = data[-2].split(ft)[-1]
    p = image[:5]
    image_data = image[head_size:]
    y = int.from_bytes(size[-12:-8], byteorder='little')
    x = int.from_bytes(size[-8:-4], byteorder='little')

    # Сохраняет заголовок файла, без размеров текстуры и кодека
    with open(f'{name}.bin', 'wb') as head_file:

        head_data = b''

        for d in range(len(data) - 1):
            head_data += data[d] + b'\x00PTexture2D\x00'

        head_data = head_data[:-24]
        head_file.write(head_data)

    if file_type == 'dds':
        dds_save(x, y, p, name, image_data)

    elif file_type == 'png':
        bmp_save(x, y, p, name, image_data)


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
