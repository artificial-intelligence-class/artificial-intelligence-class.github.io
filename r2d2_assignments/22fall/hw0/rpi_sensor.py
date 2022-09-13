import socket
import struct
import threading
import time
from concurrent import futures
from threading import Thread

import cv2


class RPiSensor:
    def __init__(self, host, port=65432):
        self.__addr = (host, port)
        self.__so = None

    def __enter__(self):
        self.__so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__so.connect(self.__addr)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__socket.sendall(b'\xff')
        self.__so.close()
        self.__so = None

    @property
    def __socket(self):
        if self.__so is None:
            raise ConnectionError('Server is not connected')
        return self.__so

    def get_obstacle_distance(self):
        self.__socket.sendall(b'\x00')
        return struct.unpack('!f', self.__so.recv(4))[0] * 100

    def get_cliff(self):
        self.__socket.sendall(b'\x01')
        return self.__so.recv(1)[0]


class RPiCamera:
    def __init__(self, src):
        self.__src = src
        self.__capture = cv2.VideoCapture()
        self.__thread = None
        self.__running = False
        self.__queue = []
        self.__lock = threading.Lock()

    def __enter__(self):
        self.__capture.open(self.__src)
        if not self.__capture.isOpened():
            raise ConnectionError('Unable to connect to the camera')
        self.__running = True
        self.__thread = Thread(target=self.__update)
        self.__thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__running = False
        self.__thread.join()
        self.__capture.release()

    def __update(self):
        while self.__running:
            status, frame = self.__capture.read()
            if not status:
                break
            with self.__lock:
                for f in self.__queue:
                    f.set_result(frame)
                self.__queue.clear()
        with self.__lock:
            for f in self.__queue:
                f.set_exception(AttributeError('No more available frames'))
            self.__queue.clear()

    def get_frame(self, timeout=None):
        with self.__lock:
            if not self.__thread.is_alive():
                raise ConnectionError('Thread is not running')
            future = futures.Future()
            self.__queue.append(future)
        return future.result(timeout)


if __name__ == '__main__':
    # Fill in the following IP_ADDRESS with the ip address of your Raspberry Pi

    # Camera Example
    with RPiCamera('tcp://IP_ADDRESS:65433') as camera:
        while True:
            cv2.imshow('frame', camera.get_frame())
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

    # Sensor Example
    with RPiSensor('IP_ADDRESS') as sensor:
        while True:
            print(sensor.get_obstacle_distance())  # Distance to the obstacle in terms of centimeters
            print(sensor.get_cliff())  # 0 - no cliff, 1 - detected cliff
            time.sleep(1)
