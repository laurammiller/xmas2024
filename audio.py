import board
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

audio = AudioOut(board.GP2)
path = "sounds/"

def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass


play_sound("encouragement1.wav")
