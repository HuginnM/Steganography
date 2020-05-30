import os
from PIL import Image
from random import randint, seed


def encode_image():
    text_mask = 0b10000000
    text_len = os.stat(text_file).st_size
    img_len = width * height
    type_skips, num_skips = choose_number_or_random()
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
                embed_color(x, y, stego_bit)
                num_stegobits += 1
                symbol <<= 1

                if type_skips == 2:
                    num_skips = randint(r_min, r_max)


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


# Выбираем количество пропущенных пикселей для внедрения стегобита.
def choose_num_of_skips():
    num = int(input('Choose number of skips pixels for embedding stegobit:\n'
                    '(Enter "0" if you want to encode each pixel)\n'))
    return num


def choose_number_or_random():
    answer = int(input('If you want to skip a specific number of pixels, '
                       'enter - "1"\nIf you want to choose random generation '
                       'the number of skipped characters, enter - "2"\n'))
    if answer == 1:
        return answer, choose_num_of_skips()
    elif answer == 2:
        return answer, choose_seed_min_max()
    else:
        print('Wrong answer!')


def choose_seed_min_max():
    c_seed = int(input('Enter random seed:\n'))
    c_min = int(input('Enter min of random(More than 0):\n'))
    while c_min < 1:
        print('Min must be more than "0"!')
        c_min = int(input('Enter min of random(More than 0):\n'))
    c_max = int(input('Enter max of random:\n'))
    return c_seed, c_min, c_max


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
        embed_color(x, 0, int(text_len[x]))


# Функция принимает координаты пикселя и нужный бит для упаковки,
# после чего кодирует в выбранный ранее цветовой канал и изменяет пиксель.
def embed_color(x, y, stego_bit):
    new_color = [pix[x, y][0], pix[x, y][1], pix[x, y][2]]
    new_color[selected_rgb] = embed(pix[x, y][selected_rgb], stego_bit)
    new_color = tuple(new_color)
    image.putpixel((x, y), new_color)


image = Image.open('images/f35.bmp')  # Открываем изображение
text_file = 'sample.txt'
text = open(text_file, 'r')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей
selected_rgb = choose_rgb()  # Выбираем спектр, в который будем кодировать

encode_image()

image.save("images/encoded.bmp", "bmp")
text.close()
