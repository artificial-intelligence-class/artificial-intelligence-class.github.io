############################################################
# CIS 521: R2D2-Homework 1
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

from client import DroidClient
import time
from random import shuffle
import sys,tty,os,termios

############################################################
# Section 1: Let's get Rolling
############################################################

def getkey():
     old_settings = termios.tcgetattr(sys.stdin)
     tty.setcbreak(sys.stdin.fileno())
     try:
         while True:
             b = os.read(sys.stdin.fileno(), 3).decode()
             if len(b) == 3:
                 k = ord(b[2])
             else:
                 k = ord(b)
             key_mapping = {
                 127: 'backspace',
                 10: 'return',
                 32: 'space',
                 9: 'tab',
                 27: 'esc',
                 65: 'up',
                 66: 'down',
                 67: 'right',
                 68: 'left'
             }
             return key_mapping.get(k, chr(k))
     finally:
         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.',
                    'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..',
                    'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.',
                    'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
                    'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
                    '9':'----.', '0':'-----'}

class R2D2(object):

    def __init__(self, robot):
        # 0 point
        pass

    def drive_square(self):
        # 1 point
        pass

    def drive_rectangle(self):
        # 1 point
        pass

    def drive_robot(self, headings):
        # 1 point
        pass

    def drive_speedy(self, roll_commands):
        # 1 point
        pass

    def drive_polygon(self, n, speed=0.5, duration=2):
        # 1 point
        pass

    def set_colors(self, which_light='both'):
        # 0 point
        pass

    def flash_colors(self, colors, seconds=1):
        # 0 point
        pass

    def drive_with_keyboard(self, speed_increment=.1, heading_increment=45, duration=0.1):
        speed = 0
        heading = 0
        max_speed = 255
        while True:
            key = getkey()
            if key == 'esc':
                break
            elif key == 'up':
                # TODO - finish this function
                # 4 points
                pass

    def encode_in_morse_code(self, message):
        # 2 points
        pass

    def blink(self, length):
        # 0 point
        pass

    def play_message(self, message, short_length=0.1, long_length=0.3, 
                     length_between_blips=0.1, length_between_letters=0.5):
        # 2 points
        pass

def sort_lambda(roll_commands):
    # 1 point, one line
    pass