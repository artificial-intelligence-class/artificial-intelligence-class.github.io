---
layout: default
img: new_robot_2x.png
img_link: http://xkcd.com/2128/
caption: New Robot
title: CIS 521 Robot Excercise 0 "Using Python to Control R2D2" (Extra Credit)
active_tab: homework
release_date: 2020-09-01
due_date: 2020-09-30 23:59:00EDT
materials:
    - 
      name: skeleton file
      url: r2d2_hw0.py
    - 
      name: sensor file
      url: rpi_sensor.py
submission_link: https://www.gradescope.com/courses/160263
---

<!-- Check whether the assignment is ready to release -->
{% capture today %}{{'now' | date: '%s'}}{% endcapture %}
{% capture release_date %}{{page.release_date | date: '%s'}}{% endcapture %}
{% if release_date > today %} 
<div class="alert alert-danger">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}
<!-- End of check whether the assignment is up to date -->


<!-- Check whether the assignment is up to date -->
{% capture this_year %}{{'now' | date: '%Y'}}{% endcapture %}
{% capture due_year %}{{page.due_date | date: '%Y'}}{% endcapture %}
{% if this_year != due_year %} 
<div class="alert alert-danger">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}
<!-- End of check whether the assignment is up to date -->


<div class="alert alert-info">
This assignment is due on {{ page.due_date | date: "%A, %B %-d, %Y" }} before {{ page.due_date | date: "%I:%M%p" }}. 
</div>

{% if page.materials %}
<div class="alert alert-info">
You can download the materials for this assignment here:
<ul>
{% for item in page.materials %}
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}

# Robot Exercise 0: Use Python to Control R2D2

## Part 1: Setup Instructions
First make sure your Python version is greater than or equal to 3.7. Then install the Python library written for Sphero robots [spherov2.py](https://github.com/artificial-intelligence-class/spherov2.py):

```shell
pip3 install spherov2
```
We provide two approaches for you to control the R2D2 - using your own PC (with Bluetooth) and using other machines (RPi).
### Using your own PC to control the robot
Make sure there is a low energy Bluetooth adapter (Bluetooth 4.0 or above) on your computer, then install the Bluetooth library using the following command:

```shell
pip3 install bleak
```

If the installation went well, you shouldn't have to do anything else. Next, run the following code in python to control the R2D2:

```python
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

toy = scanner.find_toy()
with SpheroEduAPI(toy) as droid:
    droid.roll(0, 100, 3)
```
The robot should roll forward with speed 100 for 3 seconds. The `scanner` will find the Bluetooth address of the R2D2/R2Q5. You can also find toys using specific filters such as the ID tag on the back of the droids.

`SpheroEduAPI` is a high level API used in sending commands to the droid. Please refer to the [document](https://spherov2.readthedocs.io/en/latest/sphero_edu.html) for more information.

### Using other machines (Raspberry Pi) to control the robot
For devices that do not have Bluetooth, you can use another device (for example, the Raspberry Pi that comes with the robot) as a backup option to connect to the robot. The machine acts as a relay server between the robot and the client that runs the actual code.

To use this method, you may need some basic `ssh` knowledge, here is a [**guide**](ssh_bash_skills.md) on how to connect to the Raspberry pi.

You will need to `pip3 install bleak` on the target machine first. We have already done this for you on the RPi.

To start the server on the target server machine, run:

```shell
sudo -E python3 -m spherov2.adapter.tcp_server
```

After you have successfully launched the server, go to the python IDE and add an extra TCP adapter to the previous code:

```python
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.adapter.tcp_adapter import get_tcp_adapter

toy = scanner.find_toy(adapter=get_tcp_adapter('xxx.xxx.x.xxx')) # The IP Address of the server machine
with SpheroEduAPI(toy) as api:
    api.roll(0, 100, 3)
```

## Part 2: Let's get rolling (Practice Python Skills via R2D2) [25 points]
Now it's your turn to practice! We have provided some functions for you to implement, which will also enhance your python skills. Download the skeleton file for this section [here](r2d2_hw0.py). Please refer to this [document](https://spherov2.readthedocs.io/en/latest/sphero_edu.html) for more details of the R2-D2's API.
### 1. Lists and For loops [5 points]
Python's for loop allows us to execute a series of roll commands based on a list of triples in the form of `(heading, speed, duration)`. 

* Implement a function called `drive_with_commands` which will ask the R2-D2 to execute a list of roll commands.

```python
with SpheroEduAPI(toy) as droid:
    # Square Trajectory
    roll_commands = [(0, 100, 1), (90, 100, 1), (180, 100, 1), (270, 100, 1)]
    drive_with_commands(droid, roll_commands)

    # Pentagon Trajectory
    roll_commands = [(0, 100, 1), (72, 100, 1), (144, 100, 1), (216, 100, 1), (288, 100, 1)]
    drive_with_commands(droid, roll_commands)
```

* Write a **one-line function** `sort_lambda(roll_commands)` that uses a lambda function to first sort the `roll_commands` by duration, and then by speed, both in increasing order, and **in-place**.

### 2. Functions (Drive Regular Polygon) [5 points]
Instead of manually specifying the commands to have the robot drive in a square or a pentagon, let’s write a function that will let it drive in the shape of any regular polygon. The figure shown below describes the angle relationship of a polygon and the equation to compute the interior angle. 

* Complete the function `drive_polygon` which will let the R2D2 follow a trajectory of a polygon with `n` sides.

<p float="left">
  <img src="images/polygon.jpg" width="40%" />
  <img src="images/drive_with_polygon.gif" width="50%" /> 
</p>

### 3. Dictionaries (RGB LED) [5 points]
Python dictionaries are hash tables that let us store key-value pairs. Let's use a dictionary to map color names (Strings) to their corresponding RGB values. We'll store the RGB values as a `Color` object that indicates the intensity of each of these colors (ranging from 0 to 255). 

<p float="center">
  <img src="images/color map.png" width="40%" />
  <img src="images/rgb_fade.gif" width="55%" /> 
</p>

* We provide such a dictionary in the skeleton code. Your task is to implement the function `set_lights(color, which_light='both')` which uses the API `set_main_led()` and `set_back_led()` to change the lights of the R2D2 according to the input color. 

* It should be noted that the `color` argument could either be the color name or the hexadecimal color which means you have to write a helper function `hex2rgb()` to convert HEX to RGB. 

```python
>>> print(hex2rgb('#B4FBB8'))
Color(r=180, g=251, b=184)
```
### 4. Driving with the Keyboard Arrow Keys [10 points]
Let’s design a video game style controller for the robot, where we can use the arrow keys to change its speed (by pressing up or down) and its orientation (by pressing left or right)

* We give you a function for reading in a keystroke from the keyboard called `getkey()` and your task is to complete the `drive_with_keyboard()` function which continuously reads in the keyboard input and uses it to drive the robot. (<em>Hint: Use [`set_heading()`](https://spherov2.readthedocs.io/en/latest/sphero_edu.html#spherov2.sphero_edu.SpheroEduAPI.set_heading) and [`set_speed()`](https://spherov2.readthedocs.io/en/latest/sphero_edu.html#spherov2.sphero_edu.SpheroEduAPI.set_speed)</em>)
* Press the `up` arrow key to increase the speed by `speed_delta`, press the `down` arrow key to decrease the speed by `speed_delta`; press the `left` arrow key to decrease the heading by `heading_delta`, and press the `right` arrow key to increase the heading by `heading_delta`. Press the `esc` button to exit the keyboard driving mode.
* You are required to make a short video as a demonstration of this function. We will grade you based on the performance.

<center>
<img src="images/drive_with_keyboard.gif" class="img-responsive"/>
</center>

### 5. Sending a Message via Morse Code
In Star Wars, R2-D2 delivers a message from Princess Leia to Obi-Wan Kenobi.  Our robots can only play pre-programmed sounds, so we will use the robot's lights to blink out the message "Help me, Obi-Wan Kenobi. You're my only hope." in [Morse Code](https://en.wikipedia.org/wiki/Morse_code). See a demo below:

<center>
<img src="images/morse.gif" class="img-responsive"/>
</center>

Here we will use the Python concept of a [generator](https://wiki.python.org/moin/Generators). Generators behave similar to iterators like lists, so they can be used in Python's for loops.  They have the added nice property of creating the next item on-demand, which means that they can often be more efficient than the equivalent operation of generating a list and returning its iterator. That property is nice in this example, since the message that Leia sent to Obi-Wan is actually quite a bit longer than everyone remembers:

<blockquote style="font-size:15px">
General Kenobi. Years ago, you served my father in the Clone Wars. Now he begs you to help him in his struggle against the Empire. I regret that I am unable to present my father's request to you in person, but my ship has fallen under attack and I'm afraid my mission to bring you to Alderaan has failed. I have placed information vital to the survival of the Rebellion into the memory systems of this R2 unit. My father will know how to retrieve it. You must see this droid safely delivered to him on Alderaan. This is our most desperate hour. Help me, Obi-Wan Kenobi. You're my only hope.
</blockquote>

Implement the following functions:

```python
def encode_in_morse_code(message): 
    # TODO - yield a string of morse code (dots and dashes) for each encodable character in the message

def blink(droid, duration):
    # TODO - make the holo projector blink

def play_message(droid, message, dot_duration, dash_duration, time_between_blips, time_between_letters):
    # TODO - blink out the message on the holo projector

```
Hint: To set holo-projector on/off, do `droid.set_holo_projector_led(255)`, and `droid.set_holo_projector_led(0)`.

## Part 3: Sensor Systems
### 1. Mechanical Design
To let R2-D2 better train us to become a master in AI, we made a great upgrade to the droid which includes 3D printed armor and a strong sensor system. The diagrams shown below demonstrate the mechanical structure of the reinforced R2-D2. We add an ultrasonic sensor for detecting the obstacles ahead, an IR obstacle sensor to detect a cliff, and a camera on its head to perceive the world.
<center>
<img src="images/mechanical.png" class="img-responsive"/>
</center>

* **3D Print Mount**: It contains three parts, front mount, back mount and top hat. The front mount is connected to the R2-D2 using magnets which means you could easily remove it when necessary. The back mount and top hat are attached to the R2-D2 by glue. There is an [AprilTag](https://roboticsknowledgebase.com/wiki/sensing/apriltags/) stuck to the hat for position tracking.
* **Raspberry Pi**: The Raspberry Pi is connected to the front mount via magnets and it is powered by the LiPo battery.
* **Power Management Board**: This board is closely attached to the Raspberry Pi with screws to control the power from the LiPo battery and prevent damage caused by a short circuit.
* **LiPo Battery**: The LiPo battery is equipped on the back mount using magnets. There also exists a tiny AprilTag for position tracking.
* **Ultrasonic Sensor**: The ultrasonic sensor uses sound waves to measure the distance to obstacles, here is an [introduction](https://www.maxbotix.com/articles/how-ultrasonic-sensors-work.htm) on how it works. In our design, the ultrasonic sensor is mounted on the front armor with glue to detect the obstacles in front of the R2-D2.
* **IR Obstacle Sensor**: Instead of utilizing sound waves, the Infrared Transmitter (IR) obstacle sensor uses light radiation to perceive the obstacles. Please refer [here](https://www.electronicshub.org/ir-sensor/) for details. The IR sensor is linked to the front mount using screws and points to the ground to detect cliffs.
* **Camera**: The camera is mounted on the hat with screws which can be easily dismounted. The camera has a high resolution of 1080p/30fps. A detailed description of the camera specs can be found [here](https://www.amazon.com/Camera-Module-Raspberry-Webcam-Megapixel/dp/B07QNSJ32M/ref=pd_lpo_147_img_2/131-5121704-3399433?_encoding=UTF8&pd_rd_i=B07QNSJ32M&pd_rd_r=db2bf780-0d92-4bb7-baac-a6c85ef80149&pd_rd_w=jpCCk&pd_rd_wg=66dxv&pf_rd_p=7b36d496-f366-4631-94d3-61b87b52511b&pf_rd_r=CM3XAE7MQVH2XWJ8T55C&refRID=CM3XAE7MQVH2XWJ8T55C&th=1).
* **How to turn it on?**: There is a small button on the power management board. Press it once to start the system and double click to shut down the system.
* **How to charge?**: To charge the R2-D2, there is a micro-USB port on the lower left corner at the rear of R2-D2. To charge the Raspberry Pi, there are three micro-USB ports, two on the Raspberry Pi and one on the power management board. You should charge the battery via the one on the power management board.

### 2. Circuit Design and Control Logic
The figure below shows the circuit diagram of the sensor system. If you unplug any of these wires by mistake, you could easily fix them by following this diagram. The control logic is also demonstrated below for you to understand how the system works.

<table><tr>
<td> <img src="images/diagram.jpg" alt="Drawing" style="width: 300px;" /> </td>
<td> <img src="images/architecture.jpg" alt="Drawing" style="width: 500px;"/> </td>
</tr>
<tr>
<td style="text-align:center">Circuit Diagram</td>
<td style="text-align:center">Control Logic</td>
</tr>
</table>

#### Circuit
Here are some descriptions of the circuit diagram, refer [here](https://raspberrypi.stackexchange.com/questions/83610/gpio-pinout-orientation-raspberypi-zero-w) for the PIN layout of Raspberry Pi zero.

* **Ultrasonic Sensor** : Vcc - PIN 2, Gnd - perfboard - PIN6, Trig - PIN7 (GPIO 4), ECHO - perfboard - PIN 11 (GPIO 17).
* **IR Obstacle Sensor** : Vcc - PIN 4, Gnd - PIN 39, Out - PIN 40 (GPIO 21)

#### Control Logic

* **Raspberry Pi**: Handles signals sent from the camera and the sensors, and sends them to the PC when requested. The RPi could also work as the server to send commands to the R2-D2 if your PC does not have a Bluetooth adapter.
* **PC**: Your PC could generate target commands to the R2-D2 based on the sensor data sent from Raspberry Pi.
* **R2-D2 & Sensors**: Joined by the 3D print mount as the terminal equipment to show the functions. 

### 3. Receive the Sensor Data

Before starting this section, make sure to have successfully SSHed into the Raspberry Pi unit on the R2D2 following this [`document`](ssh_bash_skills.md). Once you've successfully SSHed into the R2D2s RPi unit, run the `ls` command. It should show you two files; `camera_server.py` and `sensor_server.py`.


Download [`rpi_sensor.py`](rpi_sensor.py) to your computer, which contains some utility functions required to receive the sensor data.

#### Camera

**On the RPI's shell terminal:**

Run the following code to start the video server.

```shell
python3 camera_server.py
```
You should see the message `Waiting for a TCP connection on x.x.x.x:65433...`.

**On your computer's shell terminal:**

Install [OpenCV](https://github.com/skvark/opencv-python) on your computer using the following command:

```shell
pip3 install opencv-python
```

Then use the given function in `rpi_sensor.py` to create and run a python script as follows:

```python
from rpi_sensor import RPiCamera
import cv2

if __name__ == '__main__':
    with RPiCamera('tcp://IP_ADDRESS:65433') as camera: # Replace IP_ADDRESS with the IP address of your Raspberry Pi
        while True:
            cv2.imshow('frame', camera.get_frame())
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
```

If every thing goes well, you will be able to see a real time video streaming window pop on your screen.

**Note:** It should be noticed that you have to start the server before running the client code.

#### Sensors

In addition to the built-in sensors [API](https://spherov2.readthedocs.io/en/latest/sphero_edu.html#sensors), we provide a server to obtain data from the ultrasonic sensor and cliff detection sensor. To start the sensor server, run the following command on the Raspberry Pi shell terminal:

```shell
python3 sensor_server.py
```

We provide an `RPiSensor` class in `rpi_sensor.py`. You could connect to the sensor server with the following code:

```python
from rpi_sensor import SensorClient

with RPiSensor('IP_ADDRESS') as sensor: # IP address of Raspberry Pi
    print(sensor.get_obstacle_distance())  # Distance to the obstacle in terms of centimeters
    print(sensor.get_cliff())  # 0 - no cliff, 1 - detected cliff
```

To fetch the ultrasonic sensor data, use the method `.get_obstacle_distance()`. Similarly, use `.get_cliff()` for cliff detection.

### Combine R2D2 with the Camera & Sensors (Surveillance Mode) [25 points]

Now it's your turn to complete the second part of the script, in which you are required to combine the `drive_with_keyboard()` function with the sensor/camera system. Inspired by the head-up display (HUD) system of jet fighter, we could display the sensor information on the video streaming window shown below.

<p float="left">
  <img src="images/HUD.jpg" width="50%" />
  <img src="images/R2D2_HUD.gif" width="49%" /> 
</p>


**Requirements**

1. Modify the `drive_with_keyboard()` function in the last section and add new commands `tab` and `return` to rotate R2-D2's head by `dome_delta` and `space` to switch between tripod and bipod modes.
2. Implement the `get_droid_info()` function which updates a global dictionary `droid_info` which contains the velocity, heading, acceleration, etc. Refer [here](https://spherov2.readthedocs.io/en/latest/sphero_edu.html#sensors) for the details of the API. Notice that the API does not provide dome angle `dome` (which is an integer) and the stance of the droid `tripod` (which is `True` if the droid is in tripod mode and `False` if it's in bipod mode). You have to record the state somewhere in your code, and update them accordingly with the keyboard commands.
3. Display the sensor data on the video streaming window. (We have done this step for you in `plot_info`, but feel free to modify it)
4. To show the performance of your implementation, you could use the save video option in the skeleton code to record the video stream. This task is graded based on the video. In order to get full credit, you have to use each command (key) **at least** once and the robot's action corresponding to the commands should be shown in the video clearly.

Once you've finished filling in these functions, you can use `start_surveillance(droid)` to start the surveillance mode and test out your implementation.
