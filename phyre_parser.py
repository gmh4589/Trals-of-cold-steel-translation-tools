import os
# from pprint import pprint
from tkinter import filedialog as fd
from PIL import Image

dir_path = ''


def name_check(name):
    a = 0
    new_name = name

    while True:
        a += 1

        if os.path.exists(f'{new_name}.dds'):
            new_name += f'{name}_{a}'
        else:
            break

    return new_name


def dds_save(x, y, codec, name, data):

    if codec == b'RGBA8':
        png_save(x, y, codec, name, BGR2RGB(data, 'ARGB'))
    elif codec == b'ARGB8':
        png_save(x, y, b'RGBA8', name, BGR2RGB(data, 'ABGR'))

    else:
        with open(f'{dir_path}/{name_check(name)}.dds', 'wb') as dds_file:
            dds_file.write(b'DDS\x20\x7C\x00\x00\x00\x07\x10\x0A\x00' +
                           x.to_bytes(4, byteorder='little') + y.to_bytes(4, byteorder='little') +
                           b'\x70\x55\x05\x00\x01\x00\x00\x00\x01' + b'\x00' * 47 +
                           b'\x20\x00\x00\x00\x04\x00\x00\x00' +
                           (codec if codec not in (b'ARGB8', b'RGBA8') else b'\x00' * 4) +
                           (b'\x00' * 4 if codec not in (b'ARGB8', b'RGBA8') else b'\x20\x00\x00\x00') +
                           (b'\x00' * 16 if codec != b'RGBA8' else b'\xFF\x00\x00\x00\x00\xFF\x00\x00\x00\x00\xFF\x00\x00\x00\x00\xFF') +
                           b'\x00' * 19 + data)


def png_save(x, y, codec, name, data):
    name = name_check(name)
    codec = codec.decode('utf-8')[:-1]
    print(codec)
    Image.frombytes(codec, (y, x), data).save(f'{dir_path}\\{name}.png')



def byte_join(r, g, b, a, color_order):
    new_data = [item for sublist in (zip(r, g, b, a) if 'A' in color_order else zip(r, g, b)) for item in sublist]
    return bytes(new_data)


# For 24 and 32 bits
def BGR2RGB(data, color_order):
    byte_array = list(data)

    a = [byte_array[g] for g in
         range(color_order.index('A'), len(byte_array), len(color_order))] if 'A' in color_order else []
    x = [byte_array[h] for h in
         range(color_order.index('X'), len(byte_array), len(color_order))] if 'X' in color_order else []
    r = [byte_array[d] for d in range(color_order.index('R'), len(byte_array), len(color_order))]
    g = [byte_array[e] for e in range(color_order.index('G'), len(byte_array), len(color_order))]
    b = [byte_array[f] for f in range(color_order.index('B'), len(byte_array), len(color_order))]

    return byte_join(r, g, b, a if 'X' not in color_order else x, color_order)


def gxt_save(name, data):
    name = f'{dir_path}\\{name_check(name)}.gxt'

    with open(name, 'wb') as gxt_file:
        gxt_file.write(data)

    os.system(f'GXTConvert.exe {name}')


def phyre_save(name):
    ext = name.split('.')[-1]

    with open(name, 'rb') as image_file:

        image_file.seek(84)
        dds_codec = image_file.read(4)

        if ext == 'dds':
            start = 128
            codec = b'ARGB8' if dds_codec == b'\x00' * 4 else dds_codec
            image_file.seek(12)
            x = int.from_bytes(image_file.read(4), byteorder='little')
            y = int.from_bytes(image_file.read(4), byteorder='little')
        elif ext == 'bmp':
            start = 150
            codec = b'ARGB8'
            x, y = Image.open(name).size
        elif ext == 'png':
            start = 0
            codec = b'ARGB8'
            x, y = Image.open(name).size
        elif ext == 'gxt':
            start = 0
            codec = b'DXT5'
            x, y = 0, 0

        image_file.seek(start)
        image_data = Image.open(name).tobytes() if ext == 'png' else image_file.read()

    bin_file = name.replace(ext, 'bin') if ' (Texture ' not in name else f"{name.split(' (Texture ')[0]}.bin"

    with open(bin_file, 'rb') as head_file:
        head_file.seek(12)
        platform = head_file.read(4)
        head_file.seek(0)
        head_data = head_file.read()

        if platform == b'11XD':  # PC
            pref = b'\x00' * 75
            postfix = b'\x48\x02\x08\x31\x00'
            codec = head_data[-5:]
            ext = head_data[-200:]
            ext = 'dds' if b'dds' in ext else 'png'
            head_data = head_data[:-76]

            if 'png' in name and ext == 'dds':
                os.system(f'texconv.exe -f {"B8G8R8A8_UNORM" if codec == b"ARGB8" else "R8G8B8A8_UNORM"} "{name}"')
                return phyre_save(name.replace('png', 'dds'))

        elif platform == b'\x01MXG':  # PS Vita
            pref = b'\x00' * 4
            postfix = b'\x4C\x02\x08\x31\x00'
            ext = 'dds'
        elif platform == b'1XNG':  # Nintendo Switch
            pref = b'\x01\x00\x00\x00'
            postfix = b'\x4E\x02\x08\x01\x00'
            ext = 'dds' if 'dds' in name else 'png'

    new_file = f"{name.split('.')[0]}.{ext}_new.phyre" if ' (Texture ' not in name \
        else f"{name.split(' (Texture ')[0]}.{ext}_new.phyre"

    if platform == b'\x01MXG':
        e = name.split('.')[-1]

        if e == 'png':
            print(os.path.dirname(name))
            gxt_name = bin_file.replace("bin", "gxt")
            os.system(f'texconv.exe -f {"BC3_UNORM" if codec == b"DXT5" else "BC1_UNORM"} "{name}"')
            os.system(f'psp2gxt -i "{name.replace("png", "dds")}" -o "{gxt_name}"')

            with open(gxt_name, 'rb') as gxt_data:
                new_image_data = gxt_data.read()

            with open(new_file, 'wb') as new_phyre:
                new_phyre.write(head_data + new_image_data)

        elif e == 'gxt':
            with open(new_file, 'wb') as new_phyre:
                new_phyre.write(head_data + image_data)

    else:
        with open(new_file, 'wb') as new_phyre:
            new_phyre.write(head_data + x.to_bytes(4, byteorder='little') + y.to_bytes(4, byteorder='little') +
                            pref + b'\x00PTexture2D\x00' + codec +
                            b'\x00\x08\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00' +
                            (b'\x06' if codec in (b'ARGB8', b'RGBA8') else b'\x05') +
                            b'\x00\x00\x00\x0B\x00\x00\x00\x58\x02\x00\x01\x48\x04\x01\x48' + postfix + image_data)

def select_file():

    filetypes = (('Phyre files', '*.phyre *.png *.dds *.bmp *.gxt'), ('All files', '*.*'))
    phyre_files = fd.askopenfilenames(title='Выберите Phyre файл',
                                      filetypes=filetypes)

    if phyre_files == '':
        input('Файл не выбран!')
        return
    else:
        for file in phyre_files:
            yield file


def open_file():
    global dir_path

    for phyre_file in select_file():

        if phyre_file.split('.')[-1] != 'phyre':
            phyre_save(phyre_file)

        else:
            dir_path = os.path.dirname(phyre_file)
            name = os.path.basename(phyre_file).split('.')[0]

            if 'dds' in phyre_file:
                ft = b'dds\x00'
                file_type = 'dds'
                head_size = 42
            elif 'png' in phyre_file:
                ft = b'png\x00'
                file_type = 'png'
                head_size = 43
            else:
                input('Неподдреживемый тип файла!')
                next(select_file())

            with open(phyre_file, 'rb') as phyre:

                phyre.seek(4)
                size = int.from_bytes(phyre.read(4), byteorder='little')
                metaSize = int.from_bytes(phyre.read(4), byteorder='little')
                platform = phyre.read(4)
                supported = [b'1XNG', b'\x01MXG', b'11XD']

                if platform == b'\x01MXG':
                    ft = b'GXT\x00'
                    file_type = 'gxt' if 'dds' in phyre_file else 'gxt_png'
                    head_size = 42 if 'dds' in phyre_file else 107

                if platform not in supported:
                    input('Неподдерживаемая платформа\n'
                          'Выберите файл для Switch, PC или Vita версии игры!')
                    next(select_file())

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

                phyre.seek(0)
                data = phyre.read().split(b'\x00PTexture2D\x00')
                image = data[-1]

            size = data[-2].split(ft)[-1]
            p = image[:5]
            image_data = image[head_size:]

            if platform == b'11XD':
                x = int.from_bytes(size[-79:-75], byteorder='little')
                y = int.from_bytes(size[-83:-79], byteorder='little')
            elif platform == b'\x01MXG':
                sizes = image[:head_size]
                p = sizes[:5]
                x = int.from_bytes(sizes[99:101], byteorder='little')
                y = int.from_bytes(sizes[101:103], byteorder='little')
            else:
                x = int.from_bytes(size[-8:-4], byteorder='little')
                y = int.from_bytes(size[-12:-8], byteorder='little')

            # print(x, y)

            # Сохраняет заголовок файла, без размеров текстуры и кодека
            with open(f'{dir_path}\\{name}.bin', 'wb') as head_file:

                head_data = b''

                for d in range(len(data) - 1):
                    head_data += data[d] + b'\x00PTexture2D\x00'

                head_data = head_data[:-24]

                if platform == b'11XD':
                    head_file.write(head_data)
                elif platform == b'1XNG':
                    head_file.write(head_data + p)
                elif platform == b'\x01MXG':
                    head_file.write(head_data + b'\x00' * 13 + b'PTexture2D\x00' + image[:head_size])

            if file_type == 'dds':
                dds_save(x, y, p, name, image_data)
            elif file_type == 'png' or file_type == 'gxt_png':
                png_save(x, y, p, name, image_data)
            elif file_type == 'gxt':
                gxt_save(name, image_data)


if __name__ == "__main__":
    open_file()
