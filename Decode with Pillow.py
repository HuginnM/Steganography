import os
from PIL import Image
from random import randint, seed


def decode_image():
    amount_symbols = num_of_symbols()
    recorded_symbols = 0
    symbol = 0
    counter = -1
    num_stegobits = 0  # Количество записанных стегобитов
    type_skips, num_skips = choose_number_or_random()
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

            if recorded_symbols >= amount_symbols:
                print('Text has been decoded successfully!')
                return True

            counter += 1

            if counter % num_skips != 0:
                continue

            # Записываем извлечённый стегобит в символ
            symbol <<= 1
            symbol |= extract_stego_bit(x, y)
            num_stegobits += 1

            if num_stegobits % 8 == 0:
                if chr(symbol) == '\n' and len(os.linesep) == 2:
                    recorded_symbols += 1

                text.write(chr(symbol))
                recorded_symbols += 1
                symbol = 0

            if type_skips == 2:
                num_skips = randint(r_min, r_max)


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


# Выбираем количество пропущенных пикселей для внедрения стегобита.
def choose_num_of_skips():
    num = int(input('Choose number of skips pixels for embedding stegobit:\n'))
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


def num_of_symbols():
    num_str = ''
    for x in range(32):
        num_str += str(extract_stego_bit(x, 0))
    return int(num_str, 2)


def extract_stego_bit(x, y):
    return pix[x, y][selected_rgb] & 1


image = Image.open('images/encoded.bmp')  # Открываем изображение
text_file = 'result.txt'
text = open(text_file, 'w', encoding='utf-8')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей
selected_rgb = choose_rgb()  # Выбираем спектр, в который будем кодировать

decode_image()

text.close()
