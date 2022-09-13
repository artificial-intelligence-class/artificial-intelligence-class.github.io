import threading
from itertools import product

import cv2
from pupil_apriltags import Detector

from r2d2_hw2 import *
from rpi_sensor import RPiCamera

camera_params = [1388., 1398., 507., 364.]
K = np.array([[1388., 0., 507.], [0., 1398., 364.], [0., 0., 1.]])


class ARMaze:
    def __init__(self, rows=10, cols=10):
        row_lim = rows // 2
        col_lim = cols // 2
        self.__rows = rows
        self.__cols = cols
        self.__mouse_pos = (0, 0)
        self.__grids = list(product(range(row_lim - rows, row_lim + 1), range(col_lim - cols, col_lim + 1), (0,)))
        self.__2d_pts = None
        self.__obstacles = set()
        self.__start = None
        self.__goals = set()
        self.__path = None
        self.__thread = None

    def __mouse_event(self, event, x, y, *_):
        coord = (x, y)
        if event == cv2.EVENT_MOUSEMOVE:
            self.__mouse_pos = coord
        if self.__2d_pts and not self.__thread:
            if event == cv2.EVENT_LBUTTONDOWN:
                relative = convert_2d_to_relative(coord, self.__reshaped_pts)
                if relative not in self.__obstacles:
                    self.__start = relative
                    self.__path = None
            elif event == cv2.EVENT_RBUTTONDOWN:
                relative = convert_2d_to_relative(coord, self.__reshaped_pts)
                if relative not in self.__obstacles:
                    if relative and relative not in self.__goals:
                        self.__goals.add(relative)
                    else:
                        self.__goals.discard(relative)
                    self.__path = None

    def __get_xy(self, x, y):
        return self.__2d_pts[x * (self.__cols + 1) + y]

    def __xy_to_world(self, x, y):
        return x - self.__rows + self.__rows // 2 + .5, y - self.__cols + self.__cols // 2 + .5, 0

    def __generate_path(self):
        vertices = set(product(range(self.__rows), range(self.__cols))) - self.__obstacles
        edges = set()
        for vertex in vertices:
            for move in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                next_vertex = vertex[0] + move[0], vertex[1] + move[1]
                if next_vertex in vertices:
                    edges.add((vertex, next_vertex))
        return Graph(vertices, edges).tsp(self.__start, self.__goals)

    @property
    def __reshaped_pts(self):
        return [
            [self.__2d_pts[i * (self.__cols + 1) + j] for j in range(self.__cols + 1)] for i in range(self.__rows + 1)]

    def show_window(self):
        at_detector = Detector('tag36h11')
        # r2d2_detector = Detector(families='tag25h9', quad_decimate=1.0)
        cv2.namedWindow('Maze')
        cv2.setMouseCallback('Maze', self.__mouse_event)
        in_freeze = False
        freeze = None

        with RPiCamera('tcp://IP_ADDRESS:65433') as camera:  # FIXME: replace IP_ADDRESS
            while True:
                if self.__thread:
                    if not self.__thread.is_alive():
                        self.__thread.join()
                        self.__thread = None
                if in_freeze:
                    if freeze is None:
                        freeze = camera.get_frame()
                    img = freeze.copy()
                else:
                    img = camera.get_frame()
                tags = at_detector.detect(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), True, camera_params, .5)
                self.__2d_pts = None
                if len(tags) != 0:
                    tag = tags[0]
                    p = get_transformation(K, tag.pose_R, tag.pose_t)
                    self.__2d_pts = convert_3d_to_2d(p, self.__grids)
                    for pt in self.__2d_pts:
                        cv2.circle(img, pt, 1, (0, 255, 0), 1)

                    overlay = img.copy()
                    for x, y in self.__obstacles:
                        cv2.fillPoly(overlay, np.array([
                            [self.__get_xy(x, y), self.__get_xy(x + 1, y), self.__get_xy(x + 1, y + 1),
                             self.__get_xy(x, y + 1)]]), (255, 100, 100))
                    img = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

                    if self.__start is not None:
                        cv2.circle(img, convert_3d_to_2d(p, [self.__xy_to_world(*self.__start)])[0], 5, (255, 0, 0), 5)
                    if self.__goals:
                        for goal in convert_3d_to_2d(p, list(map(lambda t: self.__xy_to_world(*t), self.__goals))):
                            cv2.circle(img, goal, 5, (0, 0, 255), 5)
                    if self.__path is not None:
                        order = convert_3d_to_2d(p, list(map(lambda t: self.__xy_to_world(*t), self.__path[0])))
                        path = convert_3d_to_2d(p, list(map(lambda t: self.__xy_to_world(*t), self.__path[1])))
                        for f, t in zip(path, path[1:]):
                            cv2.arrowedLine(img, f, t, (0, 255, 0), 2)
                        for i, v in enumerate(order):
                            cv2.putText(img, str(i + 1), v, cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

                cv2.imshow('Maze', img)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
                elif self.__thread:
                    continue
                elif key == ord('f'):
                    in_freeze = not in_freeze
                    freeze = None
                elif self.__2d_pts is not None and key == ord('b'):
                    pt = convert_2d_to_relative(self.__mouse_pos, self.__reshaped_pts)
                    if pt == self.__start:
                        self.__start = None
                    self.__goals.discard(pt)
                    if pt in self.__obstacles:
                        self.__obstacles.discard(pt)
                    elif pt:
                        self.__obstacles.add(pt)
                    self.__path = None
                elif key == ord('s'):
                    if not self.__start:
                        print('No start point selected!')
                        continue
                    if not self.__goals:
                        print('No goal points selected!')
                        continue
                    self.__path = self.__generate_path()
                elif key == ord('r'):
                    if not self.__path:
                        print('No path calculated!')
                    else:
                        self.__thread = threading.Thread(target=droid_roll, args=(self.__path[1],)).start()

        cv2.destroyAllWindows()
        if self.__thread:
            self.__thread.join()


# https://youtu.be/fF-ehLFGfH0
if __name__ == '__main__':
    ARMaze().show_window()
