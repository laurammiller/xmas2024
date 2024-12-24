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

def play(filename):
    with open(path + filename, "rb") as mp3:
        decoder.file = mp3
        audio.play(decoder)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)
BLUE = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (255, 0, 0)

while True:
    gesture = apds.gesture()

    if gesture == 0x01:
        print("up")
        color_chase(BLUE, 0.01)
        #play("EPBlue8.mp3")
        mp3 = open(path + "EPBlue8.mp3", "rb")
        decoder.file = mp3
        audio.play(decoder)
        while audio.playing:
            pass
            color_chase(WHITE, 0.1)
            color_chase(BLUE, 0.1)
    elif gesture == 0x02:
        print("down")
        pixels.fill((0, 0, 255))
        play_sound("wand.wav")
    elif gesture == 0x03:
        print("left")
        pixels.fill((0, 255, 0))
        play_sound("encouragement1.wav")
    elif gesture == 0x04:
        print("right")
        pixels.fill((255, 0, 0))
        play_sound("encouragement2.wav")
# Write your code here :-)
