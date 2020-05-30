import os
import sys


BMP_HEADER_SIZE = 54


def encode_image(input_img_name, output_img_name, txt_file, degree):

    if degree not in [1, 2, 4, 8]:
        print("Degree value can be only 1/2/4/8")
        return False

    text_len = os.stat(txt_file).st_size
    img_len = os.stat(input_img_name).st_size

    if text_len >= img_len * degree / 8 - BMP_HEADER_SIZE:
        print("Too long text")
        return False

    text = open(txt_file, 'r')
    input_image = open(input_img_name, 'rb')
    output_image = open(output_img_name, 'wb')

    bmp_header = input_image.read(BMP_HEADER_SIZE)
    output_image.write(bmp_header)

    text_mask, img_mask = create_masks(degree)

    while True:
        symbol = text.read(1)
        if not symbol:
            break
        symbol = ord(symbol)

        for byte_amount in range(0, 8, degree):
            img_byte = int.from_bytes(input_image.read(1), sys.byteorder) &\
                       img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree)
            img_byte |= bits

            output_image.write(img_byte.to_bytes(1, sys.byteorder))
            symbol <<= degree

    output_image.write(input_image.read())

    text.close()
    input_image.close()
    output_image.close()

    return True


def decode_image(encoded_img, output_txt, symbols_to_read, degree):
    if degree not in [1, 2, 4, 8]:
        print("Degree value can be only 1/2/4/8")
        return False

    img_len = os.stat(encoded_img).st_size

    if symbols_to_read >= img_len * degree / 8 - BMP_HEADER_SIZE:
        print("Too much symbols to read")
        return False

    text = open(output_txt, 'w', encoding='utf-8')
    encoded_bmp = open(encoded_img, 'rb')

    encoded_bmp.seek(BMP_HEADER_SIZE)

    _, img_mask = create_masks(degree)
    img_mask = ~img_mask

    read = 0
    while read < symbols_to_read:
        symbol = 0

        for bits_read in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) &\
                       img_mask
            symbol <<= degree
            symbol |= img_byte

        if chr(symbol) == '\n' and len(os.linesep) == 2:
            read += 1

        read += 1
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()
    return True


def create_masks(degree):
    text_mask = 0b11111111
    img_mask = 0b11111111

    text_mask <<= (8 - degree)
    text_mask %= 256
    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask


def start():
    while True:
        choice = int(input("Enter number: 1 - encode, 2 - decode, 3 - quit\n"))

        if choice == 1:
            encode_image(image_file, "encoded.bmp", text_file, degree)
        elif choice == 2:
            decode_image("encoded.bmp", "result.txt", to_read, degree)
        elif choice == 3:
            break
        else:
            print("Unknown command")


text_file = "sample.txt"
image_file = "matrix.bmp"
to_read = os.stat(text_file).st_size
degree = int(input("Enter degree if encoding: 1/2/4/8:\n"))
start()
