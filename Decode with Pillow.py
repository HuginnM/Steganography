import os
from PIL import Image


def decode_image():
    amount_symbols = num_of_symbols()
    recorded_symbols = 0
    symbol = 0
    counter = 1
    for y in range(height):
        for x in range(width):
            if y == 0 and x < 32:  # Пропускаем сообщение о количестве
                continue  # символов в тексте

            if recorded_symbols >= amount_symbols:
                print('Text has been decoded successfully!')
                return True

            symbol <<= 1
            symbol |= extract_stego_bit(x, y)

            if counter % 8 == 0:
                if chr(symbol) == '\n' and len(os.linesep) == 2:
                    recorded_symbols += 1
                text.write(chr(symbol))
                recorded_symbols += 1
                symbol = 0

            counter += 1


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


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
