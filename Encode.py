import os
from PIL import Image
from random import randint, seed


def encode_image():
    text_mask = 0b10000000
    text_len = os.stat(text_file).st_size
    img_len = width * height
    color_list, r_seed, r_min, r_max = choose_stego_key()
    col_len = len(color_list)
    seed(r_seed)
    possible_symbols = (img_len - 32) // (r_max - r_min)
    num_skips = randint(r_min, r_max)

    if text_len > possible_symbols:  # Определяем влезет ли
        print("Too long text")       # текст в изображение
        return False

    embed_len_text(text_file)

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
                        print("Text has been encoded successfully")
                        return

                    symbol = ord(symbol)

                stego_bit = symbol & text_mask
                stego_bit >>= 7
                sel_color = choose_color(counter % col_len, color_list)

                embed_color(x, y, stego_bit, sel_color)

                num_stegobits += 1
                symbol <<= 1
                num_skips = randint(r_min, r_max)


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


def embed(source_byte, stego_bit):
    if source_byte & 1 == stego_bit:
        return source_byte
    return source_byte ^ 1


#  Кодируем в начало изображения количество закодированных символов
def embed_len_text(txt_file):
    text_len = bin(os.stat(txt_file).st_size)
    text_len = text_len.replace('0b', '')
    text_len = '0'*(32 - len(text_len)) + text_len
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

encode_image()

image.save("images/encoded.bmp", "bmp")
text.close()
