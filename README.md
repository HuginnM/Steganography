# Steganography
Welcome to Steganographic data protection software system!

This system can encode your message into an image.
You can also extract your message from the image. 
These functions are divided into 2 programs.
The system has 5 functionalities:

Functionality No. 1 - we introduce secret bits
into all pixels in a row.
Stego-key = <color_channel>

Functionality No. 2 - we introduce secret bits in pixels,
 but not in everything, but with a fixed interval n.
Stego-key = <color_channel  n>

Functionality No. 3 - in contrast to the previous functionality,
the interval is not fixed, but changes at each
step of implementation.
Stego-key = <color_channel  seed  min  max>

Functionality No. 4 - includes Functionality No. 3, but
in addition, the color channel will change for each embedded
secret bit in accordance with the channel change pattern,
which looks like <RGGBBB>.
Stego-key = <color_pattern  seed  min  max>

Functionality No. 5 - has a block implementation.
This is when the secret bit is embedded not in one pixel,
but in a block of pixels. A block is a rectangular section of
an image of size K * M pixels.
Stego-key = <color_channel  K  M>
