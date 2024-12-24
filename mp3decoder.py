# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Audio Out MP3 Example"""
import board
import digitalio

from audiomp3 import MP3Decoder

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# The listed mp3files will be played in order
mp3file = "EPBlue8.mp3"
path = "sounds/"
mp3 = open(path + mp3file, "rb")
decoder = MP3Decoder(mp3)

audio = AudioOut(board.GP2)


def play(filename):
    with open(path + filename, "rb") as mp3:
        decoder = MP3Decoder(mp3)
        audio.play(decoder)
        while audio.playing:
            pass

play("EPBlue8.mp3")
print("playing")
