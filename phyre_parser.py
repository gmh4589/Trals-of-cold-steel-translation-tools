from tkinter import filedialog as fd


def open_file():
    filetypes = (('Phyre files', '*.phyre'), ('All files', '*.*'))
    phyre_file = fd.askopenfilename(title='Выберите Phyre файл',
                                    filetypes=filetypes)

    if phyre_file == '':
        print('Файл не выбран!')
        return

    file_type = phyre_file.split('.')[-2]

    if file_type == 'dds':
        file_type = b'dds\x00'
        head_size = 42
    elif file_type == 'png':
        file_type = b'png\x00'
        head_size = 43
    else:
        print('Неподдреживемый тип файла!')
        return

    with open(phyre_file, 'rb') as phyre:
        data = phyre.read().split(b'\x00PTexture2D\x00')
        image = data[-1]

    size = data[-2].split(file_type)[-1]
    sizes = []

    for i in range(0, len(size), 2):
        sizes.append(size[i:i+2])

    image_data = image[head_size:]
    sz = len(image_data)
    print(sz)

    for s in range(len(sizes) - 2):
        x = int.from_bytes(sizes[s], byteorder='little')
        y = int.from_bytes(sizes[s+2], byteorder='little')
        print(x * y)

        if x * y == sz:
            break
    else:
        print('X and Y not found...')


if __name__ == "__main__":
    open_file()
