# CIS 521: R2D2 - Homework 0
import math
import os
import sys
import threading
import time
from datetime import datetime
from typing import List, Tuple, Iterator, Dict, Any

import cv2
import numpy
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI, Stance
from spherov2.types import Color

from rpi_sensor import RPiCamera

student_name = 'Yue Yang / Hanbang Wang'

# Part 2: Let's get rolling

# Color Dictionary
color_names_to_rgb = {
    'red': Color(255, 0, 0),
    'orange': Color(255, 165, 0),
    'yellow': Color(255, 255, 0),
    'green': Color(0, 128, 0),
    'blue': Color(0, 0, 255),
    'indigo': Color(75, 0, 130),
    'violet': Color(238, 130, 238),
    'purple': Color(128, 0, 128)
}

if sys.platform.startswith('win32'):
    arrow_key_mapping = {
        72: 'up',
        80: 'down',
        77: 'right',
        75: 'left'
    }
    regular_key_mapping = {
        27: 'esc',
        9: 'tab',
        32: 'space',
        13: 'return',
        8: 'backspace'
    }

    import msvcrt


    def get_key() -> str:
        k = ord(msvcrt.getch())
        if k != 0x00 and k != 0xe0:
            return regular_key_mapping.get(k, chr(k))
        k = ord(msvcrt.getch())
        return arrow_key_mapping.get(k, None)

else:
    arrow_key_mapping = {
        65: 'up',
        66: 'down',
        67: 'right',
        68: 'left'
    }
    regular_key_mapping = {
        27: 'esc',
        9: 'tab',
        32: 'space',
        10: 'return',
        127: 'backspace'
    }

    import tty
    import termios


    def get_key() -> str:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            while True:
                b = os.read(sys.stdin.fileno(), 3).decode()
                if len(b) == 3:
                    k = ord(b[2])
                    return arrow_key_mapping.get(k, None)
                else:
                    k = ord(b)
                    return regular_key_mapping.get(k, chr(k))
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

# Morse Code Dict
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----',
    '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----'
}


# 1. Lists and For loops [5 points]
def drive_with_commands(droid: SpheroEduAPI, roll_commands: List[Tuple[int, int, int]]):
    for command in roll_commands:
        droid.roll(*command)


def sort_lambda(roll_commands: List[Tuple[int, int, int]]):
    roll_commands.sort(key=lambda e: (e[2], e[1]))


# 2. Functions (Drive Regular Polygon) [5 points]
def drive_polygon(droid: SpheroEduAPI, n: int, speed: int = 100, duration: float = 1.5):
    interior_angle = (n - 2) * 180 / n
    exterior_angle = int(180 - interior_angle)
    heading = 0
    for i in range(n):
        droid.roll(heading, speed, duration)
        heading += exterior_angle


# 3. Dictionaries (RGB LED) [5 points]
def set_lights(droid: SpheroEduAPI, color: str, which_light='both'):
    """
    :param color: a string of English name or the hex value of the color
    :param which_light: 'front' - change front only,
                        'back' - change back only,
                        'both' - change front and back
    """
    if color in color_names_to_rgb:
        color = color_names_to_rgb[color]
    elif color[0] == '#':
        color = hex2rgb(color)
    else:
        raise ValueError('Invalid color ' + color)

    if which_light in ('both', 'front'):
        droid.set_front_led(color)
    if which_light in ('both', 'back'):
        droid.set_back_led(color)


def hex2rgb(hex_code: str) -> Color:
    """convert HEX to RGB, one line"""
    return Color(*(int(hex_code[i:i + 2], 16) for i in (1, 3, 5)))


# 4. Driving with the Keyboard Arrow Keys [10 points]
def drive_with_keyboard(droid: SpheroEduAPI, speed_delta: int = 10, heading_delta: int = 30, dome_delta: int = 20):
    print('Press ESC key to exit...')
    while True:
        key = get_key()
        if key == 'esc':
            return
        elif key == 'up':
            droid.set_speed(droid.get_speed() + speed_delta)
        elif key == 'down':
            droid.set_speed(droid.get_speed() - speed_delta)
        elif key == 'left':
            droid.set_heading(droid.get_heading() - heading_delta)
        elif key == 'right':
            droid.set_heading(droid.get_heading() + heading_delta)
        elif key == 'tab':
            extra_droid_info['dome'] -= dome_delta
            droid.set_dome_position(extra_droid_info['dome'])
        elif key == 'return':
            extra_droid_info['dome'] += dome_delta
            droid.set_dome_position(extra_droid_info['dome'])
        elif key == 'space':
            extra_droid_info['tripod'] = not extra_droid_info['tripod']
            droid.set_stance(Stance.Tripod if extra_droid_info['tripod'] else Stance.Bipod)


# 5. Sending a Message via Morse Code
def encode_in_morse_code(message: str) -> Iterator[str]:
    for c in message:
        c = c.upper()
        if c in morse_code_dict:
            yield morse_code_dict[c]


def blink(droid: SpheroEduAPI, duration: float):
    droid.set_holo_projector_led(255)
    time.sleep(duration)
    droid.set_holo_projector_led(0)


def play_message(droid: SpheroEduAPI, message: str, dot_duration: float = 0.1, dash_duration: float = 0.3,
                 time_between_blips: float = 0.1, time_between_letters: float = 0.5):
    for morse_letter in encode_in_morse_code(message):
        for c in morse_letter:
            if c == '.':
                blink(droid, dot_duration)
            elif c == '-':
                blink(droid, dash_duration)
            time.sleep(time_between_blips)
        time.sleep(time_between_letters)


# Part 3: Sensor Systems
extra_droid_info = {'dome': 0, 'tripod': True}


def get_droid_info(droid: SpheroEduAPI) -> Dict[str, Any]:
    return {
        'velocity': droid.get_velocity(),
        'location': droid.get_location(),
        'distance': droid.get_distance(),
        'heading': droid.get_heading(),
        'orientation': droid.get_orientation(),
        'acceleration': droid.get_acceleration(),
        'dome': extra_droid_info['dome'],
        'gyroscope': droid.get_gyroscope(),
        'speed': droid.get_speed(),
        'tripod': extra_droid_info['tripod']
    }


def plot_info(frame: numpy.ndarray, droid_info: Dict[str, Any]) -> numpy.ndarray:
    color = (0, 255, 0)
    font = cv2.FONT_HERSHEY_PLAIN
    location_info = 'LOC: x: {0} y: {1}'.format(
        round(droid_info['location']['x'], 1),
        round(droid_info['location']['y'], 1)
    )
    cv2.putText(frame, location_info, (50, 50), font, 1, color, 1)

    velocity_info = 'VEL: x: {0} y: {1}'.format(
        round(droid_info['velocity']['x'], 1),
        round(droid_info['velocity']['y'], 1)
    )
    cv2.putText(frame, velocity_info, (50, 70), font, 1, color, 1)

    acceleration_info = 'ACC: x: {0} y: {1} z: {2}'.format(
        round(droid_info['acceleration']['x'], 1),
        round(droid_info['acceleration']['y'], 1),
        round(droid_info['acceleration']['z'], 1)
    )
    cv2.putText(frame, acceleration_info, (50, 90), font, 1, color, 1)

    cv2.putText(frame, 'TIME: ' + str(datetime.now()), (650, 50), font, 1, color, 1)

    orientation_info = 'ORI: pitch: {0} roll: {1} yaw: {2}'.format(
        round(droid_info['orientation']['pitch'], 2),
        round(droid_info['orientation']['roll'], 1),
        round(droid_info['orientation']['yaw'], 1)
    )
    cv2.putText(frame, orientation_info, (650, 70), font, 1, color, 1)

    gyroscope_info = 'GYR: x: {0} y: {1} z: {2}'.format(
        round(droid_info['gyroscope']['x'], 2),
        round(droid_info['gyroscope']['y'], 1),
        round(droid_info['gyroscope']['z'], 1)
    )
    cv2.putText(frame, gyroscope_info, (650, 90), font, 1, color, 1)

    cv2.putText(frame, 'BY: ' + student_name, (650, 110), font, 1, color, 1)

    dome_info = str(droid_info['dome'])
    cv2.rectangle(frame, (365, 125), (585, 175), color, 2)
    cv2.putText(frame, 'DOME', (440, 120), font, 2, color, 2)
    cv2.putText(frame, dome_info, (445, 165), font, 3, color, 2)

    distance_info = 'DIST: ' + str(round(droid_info['distance'], 2))
    cv2.putText(frame, distance_info, (395, 750), font, 2, color, 1)

    speed_percent = droid_info['speed'] / 255
    cv2.rectangle(frame, (100, 380), (150, 680), color, 1)
    cv2.line(frame, (80, 520), (170, 520), color, 1)
    cv2.putText(frame, 'Speed', (100, 370), font, 1, color, 1)
    cv2.putText(frame, '255', (50, 375), font, 1, color, 1)
    cv2.putText(frame, '-255', (45, 685), font, 1, color, 1)
    cv2.putText(frame, '0', (58, 525), font, 1, color, 1)
    start_point = (100, 520)
    end_point = (150, 520 - int(speed_percent * 150))
    cv2.rectangle(frame, start_point, end_point, color, cv2.FILLED)

    cv2.putText(frame, 'Heading', (785, 400), font, 2, color, 1)
    cv2.putText(frame, str(droid_info['heading']), (845, 660), font, 2, color, 1)
    cv2.circle(frame, (850, 520), 100, color, 1)
    x_offset = int(80 * math.sin(math.radians(droid_info['heading'])))
    y_offset = int(80 * math.cos(math.radians(droid_info['heading'])))
    cv2.arrowedLine(frame, (850, 520), (850 + x_offset, 520 - y_offset), color, 2)

    cv2.line(frame, (490, 350), (490, 420), color, 1)
    cv2.line(frame, (460, 384), (520, 384), color, 1)
    cv2.putText(frame, 'MODE: TRI' if droid_info['tripod'] else 'MODE: BI', (400, 680), font, 2, color, 1)

    return frame


def start_surveillance(droid: SpheroEduAPI):
    save_video = False  # change this to True to enable video saving

    with RPiCamera('tcp://IP_ADDRESS:65433') as camera:  # Replace IP_ADDRESS with the IP address of your Raspberry Pi
        drive_thread = threading.Thread(target=drive_with_keyboard, args=(droid,))
        drive_thread.start()
        if save_video:
            writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1024, 768))
        try:
            while drive_thread.is_alive():
                frame = plot_info(camera.get_frame(), get_droid_info(droid))
                cv2.imshow('HUD', frame)
                if save_video:
                    writer.write(frame)
                cv2.waitKey(1)
            cv2.destroyAllWindows()
        finally:
            if save_video:
                writer.release()
            drive_thread.join()


def main():
    # To test your function, write your test code below
    with SpheroEduAPI(scanner.find_toy()) as droid:
        drive_with_keyboard(droid)


if __name__ == '__main__':
    main()
