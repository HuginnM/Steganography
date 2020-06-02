import os
from PIL import Image
from random import randint, seed


def decode_image():
    # Задаём необходимые переменные
    color, block_width, block_height = func5_input_stego_key()
    color = choose_color(0, color)
    # Пока не получена информация о длине текста, его длиной временно будет
    # считаться 32 бита, в которых закодирована эта информация.
    amount_symbols = 32
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
            blocks_counter += 1

            if blocks_counter == 32:
                amount_symbols = int(num_str, 2)
        else:
            blocks_counter += 1

            symbol <<= 1
            symbol |= xor_block

            if blocks_counter % 8 == 0 and blocks_counter != 32:
                if chr(symbol) == '\n' and len(os.linesep) == 2:
                    recorded_symbols += 1

                text.write(chr(symbol))
                recorded_symbols += 1
                symbol = 0

            if recorded_symbols >= amount_symbols:
                print('Text has been decoded successfully!')
                return True

        # Переходим к следующему блоку
        x_img += block_width

        # Если по горизонтали закодированы все блоки, берём следующий ряд.
        if x_img + block_width - 1 >= width:
            x_img = 0
            y_img += block_height


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


def func4_input_stego_key():
    print('Enter stego key, separated by space.\n'
          'It should look like: "color_pattern random_seed rnd_min rnd_max"\n'
          'For example: "RGGBBB 1234 1 10"\nEnter stego key --> ', end='')
    input_list = list(input().split())
    col_patt = input_list[0]
    rand_seed, rand_min, rand_max = map(int, input_list[1:])
    return col_patt, rand_seed, rand_min, rand_max


def func5_input_stego_key():
    print('Enter stego key, separated by space.\n'
          'It should look like: "color_channel  block_width  block_height"\n'
          'For example: "R/G/B 3 4"\nEnter stego key --> ', end='')
    input_list = list(input().split())
    color = input_list[0]
    b_width, b_height = map(int, input_list[1:])
    return color, b_width, b_height


def choose_color(i, col_patt):
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


image = Image.open('images/encoded.bmp')  # Открываем изображение
text_file = 'result.txt'
text = open(text_file, 'w', encoding='utf-8')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

decode_image()

text.close()
