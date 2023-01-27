import RPi.GPIO as GPIO
import time
from typing import Union
from thread_manager import ThreadManager

thread = ThreadManager()

class Speaker:
    def __init__(self, speaker_gpio: int = 24):
        self.SPEAKERPORT = speaker_gpio
        self.NOTES = {'A2': -12.0, 'Bb2': -11.0, 'B2': -10.0, 'C3': -9.0, 'Db3': -8.0, 'D3': -7.0, 'Eb3': -6.0, 'E3': -5.0,
         'F3': -4.0, 'Gb3': -3.0, 'G3': -2.0, 'Ab3': -1.0, 'A3': 0.0, 'Bb3': 1.0, 'B3': 2.0, 'C4': 3.0, 'Db4': 4.0,
         'D4': 5.0, 'Eb4': 6.0, 'E4': 7.0, 'F4': 8.0, 'Gb4': 9.0, 'G4': 10.0, 'Ab4': 11.0, 'A4': 12.0, 'Bb4': 13.0,
         'B4': 14.0, 'C5': 15.0, 'Db5': 16.0, 'D5': 17.0, 'Eb5': 18.0, 'E5': 19.0, 'F5': 20.0, 'Gb5': 21.0, 'G5': 22.0,
         'Ab5': 23.0}
        self.KEYS = {'z': 'A2', 's': 'Bb2', 'x': 'B2', 'c': 'C3', 'f': 'Db3', 'v': 'D3', 'g': 'Eb3', 'b': 'E3', 'n': 'F3',
        'j': 'Gb3', 'm': 'G3', 'k': 'Ab3', 'q': 'A3', '2': 'Bb3', 'w': 'B3', 'e': 'C4', '4': 'Db4', 'r': 'D4',
        '5': 'Eb4', 't': 'E4', 'y': 'F4', '7': 'Gb4', 'u': 'G4', '8': 'Ab4', 'i': 'A4', '9': 'Bb4', 'o': 'B4',
        'p': 'C5'}
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SPEAKERPORT, GPIO.OUT)

    def __tone(self, note: str, time_play: Union[int, float] = 1):
        note = self.KEYS[note]
        frequency = 440.0 * (1.05946309435929530984310531 ** self.NOTES[note])

        p = GPIO.PWM(self.SPEAKERPORT, frequency)
        p.start(50)
        time.sleep(time_play)
        p.stop()

    def cancel_sound(self):
        self.__tone('w', time_play=1/3)
        self.__tone('q', time_play=1/3)

    def error_sound(self):
        self.__tone('g', time_play=1/3)
        self.__tone('f', time_play=1/3)

    def apply_sound(self):
        self.__tone('e', time_play=1/2)
        self.__tone('r', time_play=1/3)

    def sound(self, func):
        def wrapper(*args, **kwargs):
            @thread.to_thread
            def call():
                try:
                    func()
                    self.apply_sound()
                except:
                    self.error_sound()
            return call()

        return wrapper


