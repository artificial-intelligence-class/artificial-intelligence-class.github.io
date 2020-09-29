import math
import threading
import time
from collections import defaultdict
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from spherov2.helper import bound_value
from spherov2.sphero_edu import EventType


class VirtualDroid:
    def __init__(self, location):
        self.__location = location
        self.__speed = 0
        self.__heading = 0
        self.__running = False
        self.__thread = None
        self.__listeners = defaultdict(set)

    def roll(self, heading: int, speed: int, duration: float):
        self.__speed = bound_value(-255, speed, 255)
        self.__heading = heading % 360
        if speed < 0:
            self.__heading = (self.__heading + 180) % 360
        time.sleep(duration)
        self.stop_roll()

    def stop_roll(self, heading: int = None):
        if heading is not None:
            self.__heading = heading % 360
        self.__speed = 0

    def set_main_led(self, color):
        pass

    def set_heading(self, heading: int):
        self.__heading = heading % 360

    def get_heading(self):
        return self.__heading

    def set_speed(self, speed: int):
        self.__speed = bound_value(-255, speed, 255)

    def get_speed(self):
        return self.__speed

    def register_event(self, event_type: EventType, listener: Callable):
        if event_type not in EventType:
            raise ValueError(f'Event type {event_type} does not exist')
        if listener:
            self.__listeners[event_type].add(listener)
        else:
            del self.__listeners[event_type]

    @property
    def location(self):
        return self.__location

    def _update_location(self, interval: float):
        if self.__speed != 0:
            heading = math.radians(self.__heading)
            x_offset = self.__speed * interval * math.sin(heading)
            y_offset = self.__speed * interval * math.cos(heading)
            self.__location = self.__location[0] + x_offset, self.__location[1] + y_offset

    def _collision(self):
        for f in self.__listeners[EventType.on_collision]:
            threading.Thread(target=f, args=(self,)).start()


class VirtualSensor:
    CLIFF_THRESHOLD = 15

    def __init__(self, droid, obstacles, cliffs):
        self.__droid = droid
        self.obstacles = obstacles
        self.cliffs = cliffs

    def __line_intersection(self, line):
        origin = np.array(self.__droid.location, dtype=np.float)
        heading = math.radians(self.__droid.get_heading())
        point1 = np.array(line[0], dtype=np.float)
        point2 = np.array(line[1], dtype=np.float)

        v1 = origin - point1
        v2 = point2 - point1
        v3 = np.array((-math.cos(heading), math.sin(heading)), dtype=np.float)
        v4 = np.dot(v2, v3)
        if v4 != 0.:
            t1 = np.cross(v2, v1) / v4
            t2 = np.dot(v1, v3) / v4
            if t1 >= 0 and 0 <= t2 <= 1:
                return t1

    def get_obstacle_distance(self):
        minimum_dist = 200
        for obstacle in self.obstacles:
            distance = self.__line_intersection(obstacle)
            if distance is not None and distance < minimum_dist:
                minimum_dist = distance
        return minimum_dist

    def _get_cliff_distance(self):
        minimum_dist = 200
        for cliff in self.cliffs:
            distance = self.__line_intersection(cliff)
            if distance is not None and distance < minimum_dist:
                minimum_dist = distance
        return minimum_dist

    def get_cliff(self):
        return int(self._get_cliff_distance() <= self.CLIFF_THRESHOLD)


class Simulator:
    def __init__(self, location, obstacles, cliffs):
        self.droid = VirtualDroid(location)
        self.sensor = VirtualSensor(self.droid, obstacles, cliffs)
        self.__warning = None

    def update_location(self, delta):
        time.sleep(delta)
        delta = delta * 5
        plt.ion()
        plt.figure('Simulation')
        stopped = False
        speed = self.droid.get_speed()
        if self.sensor.get_obstacle_distance() < speed * delta:
            self.__warning = 'Hit obstacle!'
            self.droid._collision()
        elif not stopped:
            stopped = self.sensor._get_cliff_distance() < speed * delta
            self.__warning = 'Falls off cliff!' if stopped else None
            self.droid._update_location(delta)
        self.__plot()

    def __plot(self):
        plt.clf()
        plt.axis('equal')
        # draw obstacle
        for i, obstacle in enumerate(self.sensor.obstacles):
            plt.plot((obstacle[0][0], obstacle[1][0]), (obstacle[0][1], obstacle[1][1]), 'ro-', linewidth=2,
                     color='black', markersize=2, label=None if i else 'obstacle')
        # draw cliff
        for i, cliff in enumerate(self.sensor.cliffs):
            plt.plot((cliff[0][0], cliff[1][0]), (cliff[0][1], cliff[1][1]), 'ro-', linewidth=2, color='red',
                     markersize=5, label=None if i else 'cliff')

        distance = self.sensor.get_obstacle_distance()
        plt.text(0.25, 1.05, 'Obstacle Distance: {} cm'.format(round(distance, 1)), transform=plt.gca().transAxes,
                 fontsize=10, horizontalalignment='center')

        if self.sensor.get_cliff():
            plt.plot(*self.droid.location, color='red', markersize=15, marker='o')
            plt.text(0.75, 1.05, 'Cliff Detected: Yes', transform=plt.gca().transAxes, fontsize=10,
                     horizontalalignment='center')
        else:
            plt.plot(*self.droid.location, color='blue', markersize=15, marker='o')
            plt.text(0.75, 1.05, 'Cliff Detected: No', transform=plt.gca().transAxes, fontsize=10,
                     horizontalalignment='center')

        if self.__warning:
            plt.text(0.5, 1.1, self.__warning, transform=plt.gca().transAxes, fontsize=10, color='red',
                     horizontalalignment='center')

        if distance < 200:
            heading = math.radians(self.droid.get_heading())
            plt.quiver(*self.droid.location, math.sin(heading) * distance, math.cos(heading) * distance,
                       scale_units='xy', angles='xy', scale=1)

        plt.legend(loc='upper left', fontsize=8)
        plt.draw()
        plt.pause(0.0001)


def test_maze1():
    start_location = (85, 10)
    obstacles = (((0, 0), (0, 100)), ((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100)),
                 ((100, 30), (30, 30)), ((30, 30), (30, 70)), ((30, 70), (70, 70)), ((70, 70), (70, 55)))
    cliffs = ()
    return Simulator(start_location, obstacles, cliffs)


def test_maze2():
    start_location = (185, 15)
    obstacles = (((0, 0), (200, 0)), ((200, 0), (200, 200)), ((200, 200), (0, 200)), ((0, 200), (0, 0)),
                 ((40, 40), (200, 40)), ((40, 40), (40, 160)), ((40, 160), (160, 160)), ((160, 160), (160, 80)),
                 ((160, 80), (80, 80)), ((80, 80), (80, 120)), ((80, 120), (120, 120)))
    cliffs = ()
    return Simulator(start_location, obstacles, cliffs)


def test_maze3():
    start_location = (50, 50)
    obstacles = ()
    cliffs = (((0, 0), (0, 100)), ((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100)))
    return Simulator(start_location, obstacles, cliffs)


def test_maze4():
    start_location = (15, 15)
    obstacles = (((30, 0), (30, 100)), ((60, 180), (60, 80)), ((90, 100), (90, 0)), ((150, 100), (150, 0)),
                 ((120, 180), (120, 80)), ((-20, -20), (-20, 200)), ((-20, -20), (200, -20)),
                 ((200, 200), (200, -20)),
                 ((200, 200), (-20, 200)))
    cliffs = (((0, 0), (0, 180)), ((0, 0), (180, 0)), ((0, 180), (180, 180)), ((180, 0), (180, 180)))
    return Simulator(start_location, obstacles, cliffs)
