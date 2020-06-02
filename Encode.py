import os
from PIL import Image
from random import randint, seed


def encode_image_func1_2_3(color, num_skips, type_skips):
    possible_symbols = 0
    r_min, r_max = 1, 1

    if type_skips == 1:
        # Чтобы избежать деления на 0 и для корректного пропуска пикселей
        num_skips += 1
        # Количество возможных символов в изображении при выбранном режиме
        possible_symbols = (img_len - 32) // num_skips
    elif type_skips == 2:
        r_seed, r_min, r_max = num_skips
        seed(r_seed)
        possible_symbols = (img_len - 32) // (r_max - r_min)
        num_skips = randint(r_min, r_max)

    if text_len * 8 > possible_symbols:  # Определяем влезет ли
        print("Too long text")       # текст в изображение
        return False

    embed_len_text(len_text_bin)

    while True:
        symbol = 0
        counter = -1
        num_stegobits = 0  # Количество записанных стегобитов в символ.
        for y in range(height):
            for x in range(width):
                if y == 0 and x < 32:  # Пропускаем сообщение о количестве
                    continue           # символов в тексте

                counter += 1

                if counter % num_skips != 0:
                    continue

                if num_stegobits % 8 == 0:        # Если весь символ был
                    symbol = text.read(1)   # закодирован - берём новый.

                    if not symbol:
                        return

                    symbol = ord(symbol)

                stego_bit = symbol & text_mask
                stego_bit >>= 7
                embed_color(x, y, stego_bit, color)
                num_stegobits += 1
                symbol <<= 1

                if type_skips == 2:
                    num_skips = randint(r_min, r_max)


def encode_image_func4(color_list, r_seed, r_min, r_max):
    col_len = len(color_list)
    seed(r_seed)
    possible_symbols = (img_len - 32) // (r_max - r_min)
    num_skips = randint(r_min, r_max)

    if text_len * 8 > possible_symbols:  # Определяем влезет ли
        print("Too long text")       # текст в изображение
        return False

    embed_len_text(len_text_bin)

    while True:
        symbol = 0
        counter = -1
        num_stegobits = 0  # Количество записанных стегобитов в символ.
        for y in range(height):
            for x in range(width):
                if y == 0 and x < 32:  # Пропускаем сообщение о количестве
                    continue           # символов в тексте

                counter += 1

                if counter % num_skips != 0:
                    continue

                if num_stegobits % 8 == 0:        # Если весь символ был
                    symbol = text.read(1)   # закодирован - берём новый.

                    if not symbol:
                        return

                    symbol = ord(symbol)

                stego_bit = symbol & text_mask
                stego_bit >>= 7
                sel_color = choose_color(counter % col_len, color_list)

                embed_color(x, y, stego_bit, sel_color)

                num_stegobits += 1
                symbol <<= 1
                num_skips = randint(r_min, r_max)


def encode_image_func5(color, block_width, block_height):
    all_blocks = (width // block_width) * (height // block_height)
    blocks_counter = 0
    xor_block = 0
    symbol = 0
    x_img = 0
    y_img = 0

    if text_len * 8 + 32 > all_blocks:
        print('Too long text')
        return False

    while True:
        for y in range(block_height):
            for x in range(block_width):
                if x == 0 and y == 0:
                    xor_block = pix[x + x_img, y + y_img][color] & 1
                    continue

                extract_bit = pix[x + x_img, y + y_img][color] & 1
                xor_block ^= extract_bit

        if blocks_counter < 32:
            if int(len_text_bin[blocks_counter]) != xor_block:
                invert_bit_of_block(x_img, y_img, color)
        # Если длина текста закодирована в блоки - кодируем символы.
        else:
            if blocks_counter % 8 == 0:
                symbol = text.read(1)

                if not symbol:
                    return

                symbol = ord(symbol)

            stego_bit = symbol & text_mask
            stego_bit >>= 7

            # Здесь происходит кодирования бита в блок
            if stego_bit != xor_block:
                invert_bit_of_block(x_img, y_img, color)

            symbol <<= 1

        # Переходим к следующему блоку
        x_img += block_width

        # Если по горизонтали закодированы все блоки, берём следующий ряд.
        if x_img + block_width - 1 >= width:
            x_img = 0
            y_img += block_height

        blocks_counter += 1


def invert_bit_of_block(x, y, color):
    new_color = [pix[x, y][0], pix[x, y][1], pix[x, y][2]]
    new_color[color] = pix[x, y][color] ^ 1
    new_color = tuple(new_color)
    image.putpixel((x, y), new_color)


def embed(source_byte, stego_bit):
    if source_byte & 1 == stego_bit:
        return source_byte
    return source_byte ^ 1


# Получаем двоичную 32-х разрядную длину текста
def len_text_0bx32(txt_file):
    text_len = bin(os.stat(txt_file).st_size)
    text_len = text_len.replace('0b', '')
    text_len = '0'*(32 - len(text_len)) + text_len
    return text_len


#  Кодируем в начало изображения количество закодированных символов
def embed_len_text(text_len):
    for x in range(32):
        embed_color(x, 0, int(text_len[x]), 0)


# Функция принимает координаты пикселя и нужный бит для упаковки,
# после чего кодирует в выбранный ранее цветовой канал и изменяет пиксель.
def embed_color(x, y, stego_bit, color):
    new_color = [pix[x, y][0], pix[x, y][1], pix[x, y][2]]
    new_color[color] = embed(pix[x, y][color], stego_bit)
    new_color = tuple(new_color)
    image.putpixel((x, y), new_color)


def choose_color(i, col_patt):
    if col_patt[i] == 'R' or col_patt[i] == 'r':
        return 0
    if col_patt[i] == 'G' or col_patt[i] == 'g':
        return 1
    if col_patt[i] == 'B' or col_patt[i] == 'b':
        return 2


def func1_input_stego_key():
    print('Functionality No. 1 was selected.\n'
          'Enter Stego-key <color_channel>:\n$ ', end='')
    choose = input()
    print()
    return choose_color(0, choose), 0, 1


def func2_input_stego_key():
    print('Functionality No. 2 was selected.\n'
          'Enter Stego-key <color_channel  n>:\n$ ', end='')
    choose = list(input().split())
    print()
    return choose_color(0, choose[0]), int(choose[1]), 1


def func3_input_stego_key():
    print('Functionality No. 3 was selected.\n'
          'Enter Stego-key <color_channel  seed  min  max>:\n$ ', end='')
    choose = list(input().split())
    print()
    color = choose[0]
    rand_list = list(map(int, choose[1:]))
    return choose_color(0, color), rand_list, 2


def func4_input_stego_key():
    print('Functionality No. 4 was selected.\n'
          'Enter Stego-key <color_pattern  seed  min  max>:\n$ ', end='')
    input_list = list(input().split())
    print()
    col_patt = input_list[0]
    rand_seed, rand_min, rand_max = map(int, input_list[1:])
    return col_patt, rand_seed, rand_min, rand_max


def func5_input_stego_key():
    print('Functionality No. 5 was selected.\n'
          'Enter Stego-key <color_channel  K  M>:\n$ ', end='')
    input_list = list(input().split())
    print()
    color = input_list[0]
    b_width, b_height = map(int, input_list[1:])
    return choose_color(0, color), b_width, b_height


def choose_functionality():
    choose = 9

    while choose == 7 or choose == 9 or choose == 999:
        if choose != 7:
            print(
                '================================================================',
                '== Welcome to Steganographic data protection software system! ==',
                '================================================================',
                '\nThis program will ENCODE your message into an image.\n\n'
                'Available commands:\n'
                '1-5 - Select functionality No. (1-5) to decode your message\n'
                ' 7  - Functionality Description\n'
                ' 9  - Clear Screen\n'
                ' 0  - Exit\n', sep='\n')

            if choose == 999:
                print('== Wrong command, try again! ==\n')

        choose = int(input('Enter your choice:\n$ '))
        print()
        if choose == 1:
            a, b, c = func1_input_stego_key()
            encode_image_func1_2_3(a, b, c)
        elif choose == 2:
            a, b, c = func2_input_stego_key()
            encode_image_func1_2_3(a, b, c)
        elif choose == 3:
            a, b, c = func3_input_stego_key()
            encode_image_func1_2_3(a, b, c)
        elif choose == 4:
            a, b, c, d = func4_input_stego_key()
            encode_image_func4(a, b, c, d)
        elif choose == 5:
            a, b, c = func5_input_stego_key()
            encode_image_func5(a, b, c)
        elif choose == 7:
            print('The system has 5 functionalities:\n',
                  'Functionality No. 1:\n'
                  'Stego-key = <color_channel>\n',
                  'Functionality No. 2 - we introduce secret bits in pixels,\n'
                  'but not in everything, but with a fixed interval n.\n'
                  'Stego-key = <color_channel  n>\n',
                  'Functionality No. 3 - in contrast to the previous\n'
                  'functionality, the interval is not fixed, but changes\n'
                  'at each step of implementation.\n'
                  'Stego-key = <color_channel  seed  min  max>\n',
                  'Functionality No. 4 - includes Functionality No. 3, but\n'
                  'in addition, the color channel will change for each\n'
                  'embedded secret bit in accordance with the channel change\n'
                  'pattern, which looks like <RGGBBB>.\n'
                  'Stego-key = <color_pattern  seed  min  max>\n',
                  'Functionality No. 5 - has a block implementation.\n'
                  'This is when the secret bit is embedded not in one pixel,\n'
                  'but in a block of pixels. A block is a rectangular\n'
                  'section of an image of size K * M pixels.\n'
                  'Stego-key = <color_channel  K  M>\n', sep='\n')
        elif choose == 9:
            os.system('CLS')
        elif choose == 0:
            break
        else:
            choose = 999
            os.system('CLS')

        if 0 < choose <= 5:
            print('Text has been encoded successfully!\n')


image = Image.open('images/f35.bmp')  # Открываем изображение
text_file = 'sample.txt'
text = open(text_file, 'r')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей
text_mask = 0b10000000
text_len = os.stat(text_file).st_size
len_text_bin = len_text_0bx32(text_file)
img_len = width * height

choose_functionality()

image.save("images/encoded.bmp", "bmp")
text.close()
os.system('pause')
