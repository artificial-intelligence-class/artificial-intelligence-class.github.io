'''
  File name:r2d2_navigation_gui.py
  Author: Yue Yang
  Date: 09/30/2019
'''
import sys
import tkinter
import tkinter as tk
import tkinter.ttk
import os
from PIL import Image, ImageTk

import r2d2_hw2 as X
from r2d2_hw2 import generate_map, generate_random


class Grid(tkinter.Canvas):
    def __init__(self, master, g, rows, cols):
        if not isinstance(g, X.Graph):
            raise TypeError
        if not isinstance(rows, int):
            raise TypeError
        if not isinstance(cols, int):
            raise TypeError
        if rows < 2:
            raise ValueError
        if cols < 2:
            raise ValueError

        self.rows, self.cols = rows, cols
        self.graph = g

        self.square_half_size = int(
            min(
                40,
                int(500 / self.rows),
                int(500 / self.cols)
            ) / 2
        )

        self.square_size = self.square_half_size * 2
        print(self.square_size, self.square_half_size)

        tk.Canvas.__init__(
            self, master,
            height=self.square_size * (self.rows) + 1,
            width=self.square_size * (self.cols) + 1,
            background="white")

        self.draw_scene()

        self.allow_multi_goals = False  # user can chose multi goals
        self.can_edit = True  # user can chose another start or goals

        self.start = None
        self.goals = []
        self._tags = []

        self.bind("<Button-1>", self.left_click)
        self.bind("<Button-2>", self.right_click)
        self.bind("<Button-3>", self.right_click)
        self.focus_set()
        self.configure(highlightthickness=0)

    def draw_scene(self):
        return self.draw_scene_new()

    def draw_scene_new(self):
        # draw border

        left_up = 0, 0
        left_down = 0, self.square_size * (self.rows + 1)
        right_up = self.square_size * (self.cols + 1), 0
        right_down = self.square_size * (self.cols + 1), self.square_size * (self.rows + 1)
        self.create_line(left_up, right_up, dash=(4, 2))
        self.create_line(left_down, left_up, dash=(4, 2))

        sep = int(self.square_size / 2)

        for r in range(self.rows):
            for c in range(self.cols):
                one_self = (r, c)
                one_west_neighbour = (r, c + 1)
                one_south_neighbour = (r + 1, c)

                x0, y0 = c * self.square_size + sep, r * self.square_size + sep
                x0 = x0 + sep
                y0 = y0 + sep
                print(r, c, one_self)
                m_0 = (one_self, one_west_neighbour) in self.graph.edges
                m_1 = (one_west_neighbour, one_self) in self.graph.edges

                n_0 = (one_self, one_south_neighbour) in self.graph.edges
                n_1 = (one_south_neighbour, one_self) in self.graph.edges
                one = x0, y0

                other = x0, y0 - self.square_size
                if one_west_neighbour not in self.graph.vertics:
                    m_0 = True
                    m_1 = True

                if m_0 is True and m_1 is True:
                    self.draw_dash_line(one, other)
                elif m_0 is True and m_1 is False:
                    third = (one[0] + other[0]) / 2 + (self.square_size / 5 + 2), (one[1] + other[1]) / 2
                    self.draw_triangle(
                        (one[0], one[1] - 6,),
                        (other[0], other[1] + 6),
                        third)
                elif m_0 is False and m_1 is True:
                    third = (one[0] + other[0]) / 2 - (self.square_size / 5 + 2), (one[1] + other[1]) / 2
                    self.draw_triangle(
                        (one[0], one[1] - 6,),
                        (other[0], other[1] + 6),
                        third)
                elif m_0 is False and m_1 is False:
                    self.draw_solid_line(one, other)

                other = x0 - self.square_size, y0
                if one_south_neighbour not in self.graph.vertics:
                    n_0 = True
                    n_1 = True
                if n_0 is True and n_1 is True:
                    self.draw_dash_line(one, other)
                elif n_0 is True and n_1 is False:
                    third = (one[0] + other[0]) / 2, (one[1] + other[1]) / 2 + (self.square_size / 5 + 2)
                    self.draw_triangle(
                        (one[0]-6, one[1]),
                        (other[0]+6, other[1]),
                        third
                    )
                elif n_0 is False and n_1 is True:
                    third = (one[0] + other[0]) / 2, (one[1] + other[1]) / 2 - (self.square_size / 5 + 2)
                    self.draw_triangle(
                        (one[0] - 6, one[1]),
                        (other[0] + 6, other[1]),
                        third
                    )
                elif n_0 is False and n_1 is False:
                    self.draw_solid_line(one, other)

    def transform(self, row, col):
        x = self.square_size * col + self.square_half_size
        y = self.square_size * row + self.square_half_size
        return (x, y)

    def inverse_transform(self, event):
        row = round((event.y - self.square_half_size) / self.square_size)
        col = round((event.x - self.square_half_size) / self.square_size)
        return row, col

    def left_click(self, event):
        if self.can_edit is False:
            return
        row, col = point = self.inverse_transform(event)
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        for _ in self.goals:
            if _ == point:
                return
        self.delete("start")
        self.draw_point(point, color="red", tags="start")
        # self.drawr2d2(point)
        self.start = point

    def right_click(self, event):
        if self.can_edit is False:
            return
        row, col = point = self.inverse_transform(event)
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if point == self.start:
            return

        if self.allow_multi_goals is False:
            self.delete('goals')
            self.goals = [point]
        else:
            if point in self.goals:
                return
            self.goals.append(point)
        self.draw_point(point, color="green", tags="goals")

    def draw_point(self, point, color="black", tags=""):
        x, y = self.transform(point[0], point[1])
        radius = self.square_size / 4.0

        self._tags.append(tags)

        return self.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=color, tags=tags)

    def draw_square(self, point, color = "gray", tags = ""):
        images = []
        self._tags.append(tags)
        x, y = self.transform(point[0], point[1])
        x1 = x - 0.9 * self.square_half_size
        y1 = y - 0.9 * self.square_half_size
        x2 = x + 0.9 * self.square_half_size
        y2 = y + 0.9 * self.square_half_size
        # if 'alpha' in kwargs:
        #     alpha = int(kwargs.pop('alpha') * 255)
        #     fill = kwargs.pop('fill')
        #     fill = self.winfo_rgb(fill) + (alpha,)
        #     image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        #     print(image)
        #     images.append(ImageTk.PhotoImage(image))
        #     self.create_image(x1, y1, image=images[-1], anchor='nw')
        return self.create_rectangle(x1, y1, x2, y2, fill = color, tags = tags)
        
        
    # def drawr2d2(self, point):
    #     image = Image.open('r2d2.jpg')
    #     photo = ImageTk.PhotoImage(image)
    #     x, y = self.transform(point[0], point[1])
    #     return self.create_image(x, y, image=photo)

    def draw_number(self, point, color="black", text="", tags = ""):
        x, y = self.transform(point[0], point[1])

        return self.create_text(x, y, fill=color, font="Times 18 italic bold", text = text, tags=tags)

    def draw_line(self, p, q, color="black", width=1, arrow=None, tags=""):
        p_x, p_y = self.transform(p[0], p[1])
        q_x, q_y = self.transform(q[0], q[1])
        return self.create_line(p_x, p_y, q_x, q_y, fill=color, width=width,
                                arrow=arrow, tags=tags)

    def draw_path(self, path_ls, goals_num):
        '''can one path or multi path'''
        self.can_edit = False
        if not isinstance(path_ls, list):
            raise TypeError

        if len(path_ls) > 1:
            path = path_ls[1]
            for p, q in zip(path, path[1:]):
                self.draw_line(p, q, color="blue", width=2, arrow=tkinter.LAST,tags="path")
            if goals_num > 1:
                for i in range(1, len(path_ls[0])):
                    point = path_ls[0][i]
                    self.draw_number(point, color="white", text=str(i), tags = "path")
        else:
            path = path_ls[0]
            for p, q in zip(path, path[1:]):
                self.draw_line(p, q, color="blue", width=2, arrow=tkinter.LAST,tags="path")
                
    def clear_paths(self):
        self.can_edit = True
        self.delete("path")

    def draw_solid_line(self, p, q):
        self.create_line(
            p, q, fill="black", width=self.square_size/10, arrow=None,
                       tags="grid_line"
                       )

    def draw_dash_line(self, p, q):
        self.create_line(
            p, q, fill="black", width=1, arrow=None,
            tags="grid_line",
            dash=(4, 2),
                         )

    def draw_triangle(self, p, q, r):
        self.create_polygon(
            p, q, r,
            fill='#2683F5',
            tags="grid_line"
        )


class MainApp(tk.Tk):
    def __init__(self, g, rows, cols):
        super().__init__()
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("Grid Navigation")

        right_area = tk.Frame(self)
        right_area.grid(row=0, column=1, sticky='news')
        right_area.columnconfigure(0, weight=1)
        right_area.rowconfigure(0, weight=1)
        right_area.rowconfigure(1, weight=1)
        right_area.rowconfigure(2, weight=1)
        upper_area = tk.Frame(right_area)
        upper_area.grid(row=0, column=0, sticky='news')
        option_frame = tk.Frame(right_area)
        option_frame.grid(row=1, column=0, sticky='news')
        lower_area = tk.Frame(right_area)
        lower_area.grid(row=2, column=0, sticky='news')
        tk.Label(
            option_frame,
            text='Left click to specify the start point.\nRight click to specify the goal point.',
            justify='left'
        ).pack(padx=10, pady=10)
        self.user_choice = None
        self.user_choice_var = tk.StringVar()
        self.combobox = tk.ttk.Combobox(
            master=option_frame,
            textvariable=self.user_choice_var,
            postcommand=self.change_method,
            values=[
                'dfs',
                'bfs',
                'a_star',
                'tsp'
            ]
        )
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.change_method)
        self.combobox.current(0)
        self.user_choice = self.user_choice_var.get()

        self.label_hint = tk.Label(
            option_frame,
            justify=tk.CENTER,
            text=''
        )
        self.label_hint.pack(
            padx=10,
            pady=10
        )

        self.btn_paint = tk.Button(
            option_frame,
            text='Find Path',
            command=self.paint_path,
            width=10
        )
        self.btn_paint.pack(
            padx=10,
            pady=10,

        )

        self.btn_clear = tk.Button(
            option_frame,
            text='Clear Paths',
            command=self.clear_path,
            width=10
        )
        self.btn_clear.pack(
            padx=10,
            pady=10
        )

        self.canvas_grid = Grid(self, g, rows, cols)
        self.canvas_grid.grid(
            row=0, column=0,
            sticky='news'
        )
        self.resizable(height=False, width=False)

    def change_method(self, event=None):
        var = self.user_choice_var.get()
        print(self.combobox.current(), var)
        if self.user_choice is None:
            self.user_choice = self.user_choice_var.get()
        else:
            if self.user_choice != self.user_choice_var.get():
                self.clear_path()
                if self.user_choice_var.get() != 'tsp' and len(self.canvas_grid.goals) > 1:
                    self.canvas_grid.delete('goals')
                    self.canvas_grid.goals = []
            self.user_choice = self.user_choice_var.get()

        if self.user_choice == 'tsp':
            self.canvas_grid.allow_multi_goals = True
        else:
            self.canvas_grid.allow_multi_goals = False

    def paint_path(self):
        print('paint_path')
        if self.canvas_grid.start is None:
            return
        if not self.canvas_grid.goals:
            return
        if self.user_choice == 'tsp':
            goals_num, path_ls = X.find_path_new(graph=self.canvas_grid.graph, method=self.user_choice, start=self.canvas_grid.start,
                              goals=self.canvas_grid.goals
                              )
            self.canvas_grid.draw_path(path_ls=path_ls, goals_num = goals_num)
        else:
            goals_num, path_ls, node_visited = X.find_path_new(graph=self.canvas_grid.graph, method=self.user_choice, start=self.canvas_grid.start,
                              goals=self.canvas_grid.goals
                              )
            for node in node_visited:
                self.canvas_grid.draw_square(node, color = 'cyan', tags = 'path')
            self.canvas_grid.draw_path(path_ls=path_ls, goals_num = goals_num)
            self.canvas_grid.draw_scene()
            self.canvas_grid.draw_point(self.canvas_grid.start, color="red", tags="start")
            self.canvas_grid.draw_point(self.canvas_grid.goal, color="red", tags="start")


    def clear_path(self):
        print('clear_path')
        self.canvas_grid.clear_paths()


def calculate_distance(p, q):
    import math
    x0, y0 = p
    x1, y1 = q
    for i in [x0, x1, y0, y1]:
        if not isinstance(i, (float, int)):
            raise TypeError
    return math.sqrt(pow(x0-x1, 2) + pow(y0-y1, 2))


if __name__ == "__main__":
    rows, cols = sys.argv[1:]
    rows= int(rows)
    cols = int(cols)
    vertics, edges = generate_random(rows, cols)
    ###Test 1###
    # rows = cols = 10
    # barriers = [((3, 7), (3, 8)), ((4, 7), (4, 8)), ((5, 7), (5, 8)), ((6, 7), (6, 8)), ((7, 7), (7, 8)), ((7, 3), (8, 3)), ((7, 4), (8, 4)), ((7, 5), (8, 5)), ((7, 6), (8, 6)), ((7, 7), (8, 7))]
    # vertics, edges = generate_map(rows, cols, barriers)
    ###Test 2###
    # rows = cols = 15
    # vertics, edges = generate_map(rows, cols, [])
    # vertics, edges = generate_map(4, 4, [((1, 2), (1, 3)), ((2, 2), (2, 3)), ((2, 2), (3, 2)), ((2, 1), (3, 1))])
    graph = X.Graph(vertics, edges)
    app = MainApp(g=graph, rows = rows, cols = cols)
    app.mainloop()
