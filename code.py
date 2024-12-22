# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from adafruit_apds9960.apds9960 import APDS9960
from rainbowio import colorwheel
import neopixel

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 50

pixels = neopixel.NeoPixel(board.GP28, num_pixels)
pixels.brightness = 0.5

def rainbow(speed):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(speed)

# Initialise I2C bus.
i2c = busio.I2C(board.GP1, board.GP0)

apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE

while True:
    gesture = apds.gesture()

    if gesture == 0x01:
        print("up")
        rainbow(0)
    elif gesture == 0x02:
        print("down")
        pixels.fill((0, 0, 255))
    elif gesture == 0x03:
        print("left")
        pixels.fill((0, 255, 0))
    elif gesture == 0x04:
        print("right")
        pixels.fill((255, 0, 0))
# Write your code here :-)
