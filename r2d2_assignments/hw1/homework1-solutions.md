---
layout: default
img: python.jpg
img_link: http://xkcd.com/353/
caption: Hello world!
title: Trace Polygon Solution
active_tab: homework
---

## <a name="polygon"></a> Drive in a Regular Polygon 

For a polygon with $n$ sides, we'll need to compute what angle to turn to turn instead of 90&deg; in a square.  

<img src="image/external_angles.png" alt="Internal angle + External angle = 180 degrees" class="img-responsive" />

Here's how to compute the *interior* angle of a polygon: 
    $$ \frac{(n-2) \cdot 180}{n} $$
The angle that you want to turn the droid is the *exterior* angle.  The exterior angle is 180&deg; minus the interior angle.   Try to implement this function:

Here's the solution to the trace polygon function:

```python
def trace_polygon(n, speed=100, duration=2):
    interior_angle = (n-2)*180/n
    exterior_angle = 180-interior_angle
    heading = 0
    for i in range(n):
       print("Heading: %i" % heading)
       droid.roll(speed, heading, duration)
       heading += exterior_angle
```

## <a name="colors"></a> Set Colors

```python
import time

def set_lights(color_name, which_light='both'):
    r,g,b = color_names_to_rgb[color_name]
    if(which_light=='both'):
        droid.set_front_LED_color(r,g,b)
        droid.set_back_LED_color(r,g,b)
    elif(which_light=='front'):
        droid.set_front_LED_color(r,g,b)
    elif(which_light=='back'):
        droid.set_back_LED_color(r,g,b)


def init_color_names_to_rgb():
    color_names_to_rgb = {} 
    color_names_to_rgb['red'] = (255,0,0)
    color_names_to_rgb['orange'] = (255,165,0)
    color_names_to_rgb['yellow'] = (255,255,0)
    color_names_to_rgb['green'] = (0,128,0)
    color_names_to_rgb['blue'] = (0,0,255)
    color_names_to_rgb['indigo'] = (75,0,130)
    color_names_to_rgb['violet'] = (238,130,238)
    color_names_to_rgb['purple'] = (128,0,128)
    # More available from https://www.rapidtables.com/web/color/RGB_Color.html
    return color_names_to_rgb

def flash_colors(colors, seconds=1):
    for color_name in colors:
        set_lights(color_name, 'front')
        time.sleep(seconds)
    # TODO call the set_lights method on each color in the colors list
    # wait for the specified number of seconds in between

rainbow = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
color_names_to_rgb = init_color_names_to_rgb()
flash_colors(rainbow)
```



## <a name="keyboard"></a> Driving with the keyboard

Here is my function for driving the robot with the keyboard arrowkeys.

```python
def drive_with_keyboard(speed_increment=30, heading_increment=45, duration=0.1):
    speed = 0
    heading = 0
    max_speed = 255
    while True:
        key = getkey()
        if key == 'esc':
            break
        elif key == 'up':
            speed += speed_increment
        elif key == 'down':
            speed -= speed_increment
        elif key == 'right':
            heading += heading_increment
        elif key == 'left':
            heading -= heading_increment
        if heading >= 360:
            heading = heading % 360
        if heading < 0:
            heading = 360 + heading
        if speed >= max_speed:
            speed = max_speed
        if speed < 0: 
            speed = 0
        print("speed = %i, heading = %i" % (speed, heading))
        droid.roll(speed, heading, duration)
```

It uses the helper function `getKey()`, which is implemented like this:


First, we'll give you a function for reading in a keystroke from the keyboard.  Here it is:

```python
import sys,tty,os,termios
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
```

## <a name="morse"></a> Sending a message

```python
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.',
                    'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..',
                    'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.',
                    'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
                    'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
                    '9':'----.', '0':'-----'}

def encode_in_morse_code(message):
    for c in message:
        if c.isalnum():
            morse_letter = MORSE_CODE_DICT[c.upper()]
            yield morse_letter

def play_message(message, droid, short_length=0.1, long_length=0.3, length_between_blips=0.1, length_between_letters=0.5):
    for morse_letter in encode_in_morse_code(message):
        for dot_or_dash in morse_letter:
            if dot_or_dash == '.':
                blink(droid, short_length)
            elif dot_or_dash == '-':
                blink(droid, long_length)
            time.sleep(length_between_blips)
        time.sleep(length_between_letters)

def blink(droid, length):
    droid.set_holo_projector_intensity(1)
    time.sleep(length)
    droid.set_holo_projector_intensity(0)
```
