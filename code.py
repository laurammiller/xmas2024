import time
import board
import busio
from adafruit_apds9960.apds9960 import APDS9960
from rainbowio import colorwheel
import neopixel
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 50

pixels = neopixel.NeoPixel(board.GP28, num_pixels)
pixels.brightness = 0.5
pixels.fill((0, 0, 255))

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

audio = AudioOut(board.GP2)
path = "sounds/"

def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass

from audiomp3 import MP3Decoder

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

mp3file = "EPBlue8.mp3"
mp3 = open(path + mp3file, "rb")
decoder = MP3Decoder(mp3)

def play(filename, function):
    with open(path + filename, "rb") as mp3:
        decoder.file = mp3
        audio.play(decoder)
        while audio.playing:
            pass
            if function == 1:
                bluechaser()
            elif function == 2:
                rainbow(.1)
            elif function == 3:
                redgreen()
            elif function == 4:
                candycane()
            elif function == 5:
                insane()
            elif function == 6:
                grinch()
            elif function == 7:
                snow()
def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()

BLUE = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (255, 0, 0)
PINK = (0, 50, 200)

def rainbow(speed):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
            time.sleep(speed)
        pixels.show()

def bluechaser():
    color_chase(WHITE, 0.01)
    color_chase(BLUE, 0.02)

def redgreen():
    color_chase(RED, 0.02)
    color_chase(GREEN, 0.02)

def candycane():
    color_chase(WHITE, 0.02)
    color_chase(PINK, 0.02)

def insane():
    pixels.fill(RED)
    time.sleep(0.02)
    pixels.fill(WHITE)
    time.sleep(0.02)

def grinch():
    pixels.fill(GREEN)
    time.sleep(0.02)
    pixels.fill(WHITE)
    time.sleep(0.02)
    color_chase(GREEN, 0.02)
    pixels.fill(GREEN)
    time.sleep(0.04)
    pixels.fill(WHITE)
    time.sleep(0.02)

def snow():
    pixels.fill(WHITE)
    time.sleep(1)
    pixels.fill(BLUE)
    time.sleep(1)
Flag = False

while True:
    gesture = apds.gesture()
    Flag = not Flag

    if gesture == 0x01:
        print("up")
        if Flag:
            play("EPBlue8.mp3", 1)
        else:
            play("Rockin.mp3", 1)
    elif gesture == 0x02:
        print("down")
        pixels.fill((0, 0, 255))
        if Flag:
            play("wizard.mp3", 5)
        else:
            play("grinch.mp3", 6)
    elif gesture == 0x03:
        print("left")
        pixels.fill((0, 255, 0))
        if Flag:
            play("JingleRock.mp3", 3)
        else:
            play("Bing.mp3", 7)
    elif gesture == 0x04:
        print("right")
        pixels.fill((255, 0, 0))
        if Flag:
            play("feliz.mp3", 3)
        else:
            play("maria.mp3", 4)
# Write your code here :-)
