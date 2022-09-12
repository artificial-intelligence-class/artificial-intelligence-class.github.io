import random
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from r2d2_hw2 import *

SQUARE_SIZE = 50
TRI_HEIGHT = 15
MARGIN = 8


class Grid(tk.Canvas):
    def __init__(self, parent, vertices, edges):
        row = max(i[0] for i in vertices) + 1
        col = max(i[1] for i in vertices) + 1
        width = SQUARE_SIZE * col
        height = SQUARE_SIZE * row
        super().__init__(parent, width=width, height=height, highlightthickness=0)

        self.__graph = Graph(vertices, edges)
        self.__start = None
        self.__ends = set()
        self.__method = 'dfs'

        for vertex in vertices:
            i, j = vertex
            lx, ty, rx, by = j * SQUARE_SIZE, i * SQUARE_SIZE, (j + 1) * SQUARE_SIZE, (i + 1) * SQUARE_SIZE
            self.tag_lower(self.create_rectangle(lx, ty, rx, by, dash='.'))

            if i == 0:  # top line
                self.create_line(lx, 0, rx, 0, width=4, fill='red')

            if j == 0:  # left line
                self.create_line(0, ty, 0, by, width=4, fill='red')

            right = (i, j + 1)
            rl_edge = (right, vertex) in edges
            if (vertex, right) not in edges:
                if rl_edge:
                    self.create_polygon(rx, ty, rx, by, rx - TRI_HEIGHT, (ty + by) / 2, fill='#2683F5')
                else:
                    self.create_line(rx, ty, rx, by, width=4, fill='red')
            elif not rl_edge:
                self.create_polygon(rx, ty, rx, by, rx + TRI_HEIGHT, (ty + by) / 2, fill='#2683F5')

            down = (i + 1, j)
            du_edge = (down, vertex) in edges
            if (vertex, down) not in edges:
                if du_edge:
                    self.create_polygon(lx, by, rx, by, (lx + rx) / 2, by - TRI_HEIGHT, fill='#2683F5')
                else:
                    self.create_line(lx, by, rx, by, width=4, fill='red')
            elif not du_edge:
                self.create_polygon(lx, by, rx, by, (lx + rx) / 2, by + TRI_HEIGHT, fill='#2683F5')

        self.bind('<Button-1>', self.click)
        self.bind('<Button-2>', self.click)

    def __draw_end(self, x, y):
        self.tag_lower(self.create_oval(
            x * SQUARE_SIZE + MARGIN, y * SQUARE_SIZE + MARGIN,
            (x + 1) * SQUARE_SIZE - MARGIN, (y + 1) * SQUARE_SIZE - MARGIN,
            fill='green', tags='end', outline=''))
        self.__ends.add((y, x))

    def clear(self, method=None):
        if method:
            self.__method = method
            if method != 'tsp' and len(self.__ends) > 1:
                y, x = next(iter(self.__ends))
                self.__ends.clear()
                self.delete('end')
                self.__draw_end(x, y)

        self.delete('paths')

    def click(self, event):
        self.clear()
        x, y = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
        if event.num == 1:
            self.delete('start')
            self.tag_lower(self.create_oval(
                x * SQUARE_SIZE + MARGIN, y * SQUARE_SIZE + MARGIN,
                (x + 1) * SQUARE_SIZE - MARGIN, (y + 1) * SQUARE_SIZE - MARGIN,
                fill='red', tags='start', outline=''))
            self.__start = (y, x)
        elif event.num == 2:
            put_tag = True
            if self.__method == 'tsp':
                for item in self.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1):
                    if 'end' in self.gettags(item):
                        put_tag = False
                        self.delete(item)
                        self.__ends.discard((y, x))
                        break
            else:
                self.__ends.clear()
                self.delete('end')
            if put_tag:
                self.__draw_end(x, y)

    def search(self, method):
        self.clear(method)
        if self.__start is None:
            return messagebox.showwarning('Undefined value', 'Please select the starting point', parent=self)
        if not self.__ends:
            return messagebox.showwarning('Undefined value', 'Please select the goal point', parent=self)
        if method == 'tsp':
            opt, path = self.__graph.tsp(self.__start, self.__ends)
            if path is None:
                return messagebox.showwarning('Path does not exist', 'No path found', parent=self)
            for index, (i, j) in enumerate(opt):
                self.create_text((j + .5) * SQUARE_SIZE, (i + .5) * SQUARE_SIZE, text=index + 1,
                                 fill='white', font='Times 18 italic bold', tags='paths')
        else:
            path, nodes = getattr(self.__graph, method)(self.__start, next(iter(self.__ends)))
            if path is None:
                return messagebox.showwarning('Path does not exist', 'No path found', parent=self)
            for i, j in nodes:
                self.tag_lower(self.create_rectangle(
                    j * SQUARE_SIZE, i * SQUARE_SIZE, (j + 1) * SQUARE_SIZE, (i + 1) * SQUARE_SIZE,
                    tags='paths', fill='cyan', outline=''))

        for (i1, j1), (i2, j2) in zip(path, path[1:]):
            self.tag_raise(self.create_line(
                (j1 + .5) * SQUARE_SIZE, (i1 + .5) * SQUARE_SIZE, (j2 + .5) * SQUARE_SIZE, (i2 + .5) * SQUARE_SIZE,
                fill='blue', width=2, arrow=tk.LAST, tags='paths'))


class GUI(tk.Tk):
    def __init__(self, vertices, edges):
        super().__init__()

        self.title('Grid Navigation')
        self.__grid = Grid(self, vertices, edges)
        self.__grid.pack(side=tk.LEFT)

        right_area = tk.Frame(self)
        tk.Label(right_area,
                 text='Left click to select the start point.\nRight click to select the goal point.').pack(
            padx=10, pady=10)
        combobox = ttk.Combobox(right_area, values=['dfs', 'bfs', 'a_star', 'tsp'])
        combobox.bind('<<ComboboxSelected>>', lambda _: self.__grid.clear(combobox.get()))
        combobox.current(0)
        combobox.pack()

        btn_paint = tk.Button(
            right_area, text='Find Path', command=lambda: self.__grid.search(combobox.get()), width=10)
        btn_paint.pack(padx=10, pady=10)

        btn_clear = tk.Button(right_area, text='Clear Paths', command=self.__grid.clear, width=10)
        btn_clear.pack(padx=10, pady=10)
        right_area.pack(side=tk.RIGHT)

        self.resizable(height=False, width=False)


def generate_random(row, column):
    vertices = set((i, j) for i in range(row) for j in range(column))
    edges = set()
    for vertex in vertices:
        for move in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            next_vertex = vertex[0] + move[0], vertex[1] + move[1]
            if next_vertex in vertices:
                edges.add((vertex, next_vertex))

    num_of_barriers = row * column * 2 // 3
    barriers = random.sample(edges, num_of_barriers)
    for barrier in barriers:
        edges.discard(barrier)
        if random.random() > 0.15:
            edges.discard((barrier[1], barrier[0]))

    return vertices, edges


def custom_map():
    # vertices = {(0, 0), (0, 1), (1, 0), (1, 1)}
    # edges = {((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0))}
    vertices = set((i, j) for i in range(10) for j in range(10))
    edges = set()
    for vertex in vertices:
        for move in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            next_vertex = vertex[0] + move[0], vertex[1] + move[1]
            if next_vertex in vertices:
                edges.add((vertex, next_vertex))
    for f, t in (((3, 7), (3, 8)), ((4, 7), (4, 8)), ((5, 7), (5, 8)), ((6, 7), (6, 8)), ((7, 7), (7, 8)),
                 ((7, 3), (8, 3)), ((7, 4), (8, 4)), ((7, 5), (8, 5)), ((7, 6), (8, 6)), ((7, 7), (8, 7))):
        edges.discard((f, t))
        edges.discard((t, f))

    return vertices, edges


if __name__ == '__main__':
    if len(sys.argv) == 3:
        rows, cols = sys.argv[1:]
        rows = int(rows)
        cols = int(cols)
        vertices, edges = generate_random(rows, cols)
    else:
        vertices, edges = custom_map()
    GUI(vertices, edges).mainloop()
