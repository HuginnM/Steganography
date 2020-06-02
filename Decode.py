import os
from PIL import Image
from random import randint, seed


def decode_image_func1_2_3(color, num_skips, type_skips):
    amount_symbols = num_of_symbols()
    recorded_symbols = 0
    num_stegobits = 0  # Количество записанных стегобитов
    symbol = 0
    counter = -1
    r_min, r_max = 1, 1

    if type_skips == 1:
        # Чтобы избежать деления на 0 и для корректного пропуска пикселей
        num_skips += 1
    elif type_skips == 2:
        r_seed, r_min, r_max = num_skips
        seed(r_seed)
        num_skips = randint(r_min, r_max)

    for y in range(height):
        for x in range(width):
            if y == 0 and x < 32:  # Пропускаем сообщение о количестве
                continue  # символов в тексте

            counter += 1

            if counter % num_skips != 0:
                continue

            # Записываем извлечённый стегобит в символ
            symbol <<= 1
            symbol |= extract_stego_bit(x, y, color)
            num_stegobits += 1

            if num_stegobits % 8 == 0:
                if chr(symbol) == '\n' and len(os.linesep) == 2:
                    recorded_symbols += 1

                text.write(chr(symbol))
                recorded_symbols += 1
                symbol = 0

            if recorded_symbols >= amount_symbols:
                return True

            if type_skips == 2:
                num_skips = randint(r_min, r_max)


def decode_image_func4(color_list, r_seed, r_min, r_max):
    amount_symbols = num_of_symbols()
    recorded_symbols = 0
    symbol = 0
    counter = -1
    num_stegobits = 0  # Количество записанных стегобитов
    col_len = len(color_list)
    seed(r_seed)
    num_skips = randint(r_min, r_max)

    for y in range(height):
        for x in range(width):
            if y == 0 and x < 32:  # Пропускаем сообщение о количестве
                continue  # символов в тексте

            counter += 1
            # Если пропустили нужное количество символов - выполняем код
            if counter % num_skips != 0:
                continue

            num_skips = randint(r_min, r_max)
            color = conversion_color(counter % col_len, color_list)
            # Записываем извлечённый стегобит в символ
            symbol <<= 1
            symbol |= extract_stego_bit(x, y, color)
            num_stegobits += 1

            if num_stegobits % 8 == 0:
                if chr(symbol) == '\n' and len(os.linesep) == 2:
                    recorded_symbols += 1

                text.write(chr(symbol))
                recorded_symbols += 1
                symbol = 0

            if recorded_symbols >= amount_symbols:
                return True


def decode_image_func5(color, block_width, block_height):
    amount_symbols = 32  # Временно, пока не извлекли длину настоящую
    recorded_symbols = 0
    num_str = ''
    symbol = 0
    blocks_counter = 0
    xor_block = 0
    x_img = 0
    y_img = 0

    while True:
        for y in range(block_height):
            for x in range(block_width):
                if x == 0 and y == 0:
                    xor_block = pix[x + x_img, y + y_img][color] & 1
                    continue

                extract_bit = pix[x + x_img, y + y_img][color] & 1
                xor_block ^= extract_bit

        if blocks_counter < 32:
            num_str += str(xor_block)

            if blocks_counter == 31:
                amount_symbols = int(num_str, 2)
        else:
            symbol <<= 1
            symbol |= xor_block

            # В этот момент символ уже весь записан, но счётчик блоков
            # ещё не успел увеличится. Ловим этот момент и записываем символ.
            if blocks_counter % 8 == 7:
                if chr(symbol) == '\n' and len(os.linesep) == 2:
                    recorded_symbols += 1

                text.write(chr(symbol))
                recorded_symbols += 1
                symbol = 0

                if recorded_symbols >= amount_symbols:
                    return True

        # Переходим к следующему блоку
        x_img += block_width

        # Если по горизонтали закодированы все блоки, берём следующий ряд.
        if x_img + block_width - 1 >= width:
            x_img = 0
            y_img += block_height

        blocks_counter += 1


def conversion_color(i, col_patt):
    if col_patt[i] == 'R' or col_patt[i] == 'r':
        return 0
    if col_patt[i] == 'G' or col_patt[i] == 'g':
        return 1
    if col_patt[i] == 'B' or col_patt[i] == 'b':
        return 2


def num_of_symbols():
    num_str = ''
    for x in range(32):
        num_str += str(extract_stego_bit(x, 0, 0))
    return int(num_str, 2)


def extract_stego_bit(x, y, sel_color):
    return pix[x, y][sel_color] & 1


def func1_input_stego_key():
    print('Functionality No. 1 was selected.\n'
          'Enter Stego-key <color_channel>:\n$ ', end='')
    choose = input()
    return conversion_color(0, choose), 0, 1


def func2_input_stego_key():
    print('Functionality No. 2 was selected.\n'
          'Enter Stego-key <color_channel  n>:\n$ ', end='')
    choose = list(input().split())
    return conversion_color(0, choose[0]), int(choose[1]), 1


def func3_input_stego_key():
    print('Functionality No. 3 was selected.\n'
          'Enter Stego-key <color_channel  seed  min  max>:\n$ ', end='')
    choose = list(input().split())
    color = choose[0]
    rand_list = list(map(int, choose[1:]))
    return conversion_color(0, color), rand_list, 2


def func4_input_stego_key():
    print('Functionality No. 4 was selected.\n'
          'Enter Stego-key <color_pattern  seed  min  max>:\n$ ', end='')
    input_list = list(input().split())
    col_patt = input_list[0]
    rand_seed, rand_min, rand_max = map(int, input_list[1:])
    return col_patt, rand_seed, rand_min, rand_max


def func5_input_stego_key():
    print('Functionality No. 5 was selected.\n'
          'Enter Stego-key <color_channel  K  M>:\n$ ', end='')
    input_list = list(input().split())
    color = input_list[0]
    b_width, b_height = map(int, input_list[1:])
    return conversion_color(0, color), b_width, b_height


def choose_functionality():
    choose = 9

    while choose == 7 or choose == 9 or choose == 999:
        if choose != 7:
            print(
                '================================================================',
                '== Welcome to Steganographic data protection software system! ==',
                '================================================================',
                '\nThis program will DECODE your message into an image.\n\n'
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
            decode_image_func1_2_3(a, b, c)
        elif choose == 2:
            a, b, c = func2_input_stego_key()
            decode_image_func1_2_3(a, b, c)
        elif choose == 3:
            a, b, c = func3_input_stego_key()
            decode_image_func1_2_3(a, b, c)
        elif choose == 4:
            a, b, c, d = func4_input_stego_key()
            decode_image_func4(a, b, c, d)
        elif choose == 5:
            a, b, c = func5_input_stego_key()
            decode_image_func5(a, b, c)
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
            print('Text has been decoded successfully!\n')


image = Image.open('images/encoded.bmp')  # Открываем изображение
text_file = 'result.txt'
text = open(text_file, 'w', encoding='utf-8')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

choose_functionality()

text.close()
os.system('pause')
