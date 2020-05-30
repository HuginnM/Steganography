import os
import sys

BMP_HEADER_SIZE = 54


def encode_image(input_img_name, output_img_name, txt_file):
    text_mask = 0b10000000
    img_mask = 0b11111110

    text_len = os.stat(txt_file).st_size
    img_len = os.stat(input_img_name).st_size

    if text_len >= img_len / 24 - BMP_HEADER_SIZE:
        print("Too long text")
        return False

    text = open(txt_file, 'r')
    input_image = open(input_img_name, 'rb')
    output_image = open(output_img_name, 'wb')
    selected_rgb = choose_rgb()

    bmp_header = input_image.read(BMP_HEADER_SIZE + selected_rgb)
    output_image.write(bmp_header)

    while True:
        symbol = text.read(1)
        if not symbol:
            break
        symbol = ord(symbol)

        for byte_amount in range(0, 8):
            img_byte = int.from_bytes(input_image.read(1), sys.byteorder) &\
                       img_mask
            bits = symbol & text_mask
            bits >>= 7
            img_byte |= bits

            output_image.write(img_byte.to_bytes(1, sys.byteorder))
            output_image.write(input_image.read(2))
            symbol <<= 1

    output_image.write(input_image.read())

    text.close()
    input_image.close()
    output_image.close()
    print("Text has been encoded successfully")

    return True


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


text_file = "sample.txt"
image_file = "matrix.bmp"
encode_image(image_file, "encoded.bmp", text_file)
