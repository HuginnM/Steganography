import os
from PIL import Image
from random import randint, seed


def decode_image():
    amount_symbols = num_of_symbols()
    recorded_symbols = 0
    symbol = 0
    counter = -1
    num_stegobits = 0  # Количество записанных стегобитов

    color_list, r_seed, r_min, r_max = choose_stego_key()
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
            color = choose_color(counter % col_len, color_list)
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
                print('Text has been decoded successfully!')
                return True


def choose_stego_key():
    print('Enter stego key, separated by space.\n'
          'It should look like: "color_pattern random_seed rnd_min rnd_max"\n'
          'For example: "RGGBBB 1234 1 10"\nEnter stego key --> ', end='')
    input_list = list(input().split())
    col_patt = input_list[0]
    rand_seed, rand_min, rand_max = map(int, input_list[1:])
    return col_patt, rand_seed, rand_min, rand_max


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
