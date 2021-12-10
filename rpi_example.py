# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
pixels_per_strand = 50
num_strands = 11
num_pixels = pixels_per_strand * num_strands 

# colors
RED = (0, 255, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (64, 255, 0)
PURPLE = (0, 255, 150)

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
                           pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        if wait:
            time.sleep(wait)


def color_strand(index, color):
    light_num = index * pixels_per_strand  # 50 pixels per strand
    for i in range(light_num, light_num + pixels_per_strand):
        pixels[i] = color

def rg_dance(steps=100, pause_seconds=1):
    colors = [RED, GREEN]
    for i in range(steps):
        for strand_num in range(num_strands):
            color = colors[(i+strand_num) % len(colors)]
            color_strand(strand_num, color)
        pixels.show()
        time.sleep(pause_seconds)

def zipline(start_color, end_color, pause_seconds=None, unzip=False):
    pixels.fill(start_color)
    for i in range(num_pixels):
        pixels[i] = end_color
        pixels.show()
        if pause_seconds:
            time.sleep(pause_seconds)

    if unzip:
        zipline(end_color, start_color, pause_seconds, False)


def alternate(first_color, second_color, pause_seconds=1, num_alternations=20):
    for iteration in range(num_alternations):
        for i in range(num_pixels):
            pixels[i] = first_color if i%2==iteration%2 else second_color
        pixels.show()
        time.sleep(pause_seconds)

while True:
    # rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step

    rg_dance(steps=20)
    zipline(RED, GREEN) 
    alternate(RED, GREEN)
    rainbow_cycle(0)
    rainbow_cycle(0)
