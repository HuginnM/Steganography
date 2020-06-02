import os
from PIL import Image
from random import randint, seed


def encode_image_func5():
    # Задаём необходимые переменные
    text_mask = 0b10000000
    text_len = os.stat(text_file).st_size
    len_text_bin = len_text_0bx32(text_file)
    color, block_width, block_height = func5_input_stego_key()
    color = choose_color(0, color)
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
                    print("Text has been encoded successfully")
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


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


def choose_color(i, col_patt):
    if col_patt[i] == 'R' or col_patt[i] == 'r':
        return 0
    if col_patt[i] == 'G' or col_patt[i] == 'g':
        return 1
    if col_patt[i] == 'B' or col_patt[i] == 'b':
        return 2


def func5_input_stego_key():
    print('Enter stego key, separated by space.\n'
          'It should look like: "color_channel  block_width  block_height"\n'
          'For example: "R/G/B 3 4"\nEnter stego key --> ', end='')
    input_list = list(input().split())
    color = input_list[0]
    b_width, b_height = map(int, input_list[1:])
    return color, b_width, b_height


def invert_bit_of_block(x, y, color):
    new_color = [pix[x, y][0], pix[x, y][1], pix[x, y][2]]
    new_color[color] = pix[x, y][color] ^ 1
    new_color = tuple(new_color)
    image.putpixel((x, y), new_color)


def func4_input_stego_key():
    print('Enter stego key, separated by space.\n'
          'It should look like: "color_pattern random_seed rnd_min rnd_max"\n'
          'For example: "RGGBBB 1234 1 10"\nEnter stego key --> ', end='')
    input_list = list(input().split())
    col_patt = input_list[0]
    rand_seed, rand_min, rand_max = map(int, input_list[1:])
    return col_patt, rand_seed, rand_min, rand_max


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


image = Image.open('images/f35.bmp')  # Открываем изображение
text_file = 'sample.txt'
text = open(text_file, 'r')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

encode_image_func5()

image.save("images/encoded.bmp", "bmp")
text.close()
