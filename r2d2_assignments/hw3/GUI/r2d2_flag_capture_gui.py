import tkinter as tk
import tkinter.messagebox
import tkinter.ttk
import time
import threading
import queue
import sys
import os
import random
from PIL import Image, ImageTk
from r2d2_hw3 import generate_map, generate_random
from r2d2_hw3 import FlagCaptureGraph as Graph
import pickle
import copy

base_dir = os.path.abspath(os.path.dirname(__file__))


images = {
    'D2_1': os.path.join(base_dir, 'image', 'd2_1.png'),
    'D2_2': os.path.join(base_dir, 'image', 'd2_2.png'),
    'Q5_1': os.path.join(base_dir, 'image', 'q5_1.png'),
    'Q5_2': os.path.join(base_dir, 'image', 'q5_2.png'),
    'flag_D2': os.path.join(base_dir, 'image', 'd2_flag.png'),
    'flag_Q5': os.path.join(base_dir, 'image', 'q5_flag.png'),
}


def best_fit(window_size, image_size):
    window_width, window_height = window_size
    image_with, image_height = image_size

    if window_width / window_height <= image_with / image_height:
        dim = window_width, int(window_width * (image_height / image_with))
    else:
        dim = int(image_with / image_height * window_height), window_height

    return dim


def validate_int(var):
    '''validate 0 or positive int'''
    if not isinstance(var, tk.StringVar):
        raise TypeError
    new_value = var.get()
    old_value = new_value[:-1]
    try:
        int(new_value)
    except (TypeError, ValueError):
        var.set(old_value)


class Board(tk.Canvas):
    def __init__(self, master, rows, cols, graph, q, *args, **kwargs):
        if not isinstance(rows, int):
            raise TypeError
        if not isinstance(cols, int):
            raise TypeError
        if rows < 2:
            raise ValueError
        if cols < 2:
            raise ValueError
        if not isinstance(q, queue.Queue):
            raise TypeError
        self.q = q
        self.rows, self.cols = rows, cols
        self.square_half_size = int(
            max(
                40,
                int(500 / self.rows),
                int(500 / self.cols)
            ) / 2
        )
        self.square_size = self.square_half_size * 2

        super().__init__(
            master=master,
            height=self.square_size * self.rows,
            width=self.square_size * self.cols,
            background="white",
            *args, **kwargs)

        if not isinstance(graph, Graph):
            raise TypeError

        self.can_edit = False

        self.graph = graph

        self.images = {
            k: self.process_image(img_path=images[k]) for k in images
        }

        self.bind("<Button-1>", self.left_click)

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
            return None, None
        print(row, col)
        if (row, col) in list(self.graph.robots_pos.values()) + list(self.graph.flags_pos.values()):
            print('position taken')
            return None, None
        self.q.put(point)
        return row, col

    def process_image(self, img_path):
        if not os.path.exists(img_path):
            print(img_path)
            raise FileNotFoundError
        im = Image.open(fp=img_path)
        dim = best_fit(
            window_size=(self.square_size, self.square_size),
            image_size=im.size
                       )
        print(im.size, dim)
        im = im.resize(size=dim, resample=Image.ANTIALIAS)

        return ImageTk.PhotoImage(image=im)

    def draw_scene(self):
        ''''''

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
                        (one[0] - 6, one[1]),
                        (other[0] + 6, other[1]),
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

    def draw_text(self, row_col: tuple, text: str, tag: str, fill: str):
        x = row_col[1] * self.square_size + self.square_half_size
        y = row_col[0] * self.square_size + self.square_half_size
        # canvas_id = self.create_text(x, y, anchor='center', text=text, fill=fill, tag=tag)
        # print(canvas_id)
        self.draw_image(pos=(x, y), name=tag)

    def draw_image(self, pos, name):
        self.create_image(pos, anchor='center', image=self.images[name], tag=name)

    def draw_flags(self, row_col, tag_aft):
        text = '⚑'
        tag = 'flag_{}'.format(tag_aft)
        if tag_aft == 'D2':
            fill = 'red'
        elif tag_aft == 'Q5':
            fill = 'blue'
        else:
            raise ValueError
        self.graph.flags_pos[tag] = row_col
        return self.draw_text(row_col=row_col, text=text, tag=tag, fill=fill)

    def draw_robot(self, row_col, tag_aft):
        if not isinstance(row_col, tuple):
            raise TypeError
        if not isinstance(tag_aft, str):
            raise TypeError
        if tag_aft.startswith('D2'):
            fill = 'red'
        elif tag_aft.startswith('Q5'):
            fill = 'blue'
        else:
            raise ValueError
        if tag_aft.endswith('1'):
            text = '➀'
        elif tag_aft.endswith('2'):
            text = '➁'
        else:
            raise ValueError
        self.graph.robots_pos[tag_aft] = row_col
        return self.draw_text(row_col=row_col, text=text, tag=tag_aft, fill=fill)

    def update_robot(self, name):
        pos = self.graph.robots_pos[name]
        print('update {} to {}'.format(name, pos))
        self.delete(name)
        self.draw_robot(row_col=pos, tag_aft=name)

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


class MainGuiApp(tk.Tk):
    def __init__(self, rows=8, cols=8):
        if not isinstance(rows, int):
            raise TypeError
        if not isinstance(cols, int):
            raise TypeError

        if rows < 2:
            raise ValueError
        if rows < 2:
            raise ValueError

        super().__init__()
        self.config(bg='white')

        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Config', command=self.switch_to_config_frame)
        file_menu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)

        self.config(menu=menubar)

        self.rows = rows
        self.cols = cols
        self.first = None

        self.rows_var = tk.StringVar(value=rows)
        self.rows_var.trace('w', lambda nm, idx, mode, var=self.rows_var: validate_int(var))
        self.cols_var = tk.StringVar(value=cols)
        self.cols_var.trace('w', lambda nm, idx, mode, var=self.cols_var: validate_int(var))
        self.first_var = tk.StringVar()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.graph_table = self.load_scenes()
        self.game_scenes = []
        for i in self.graph_table:
            self.game_scenes.append(i[0])
        self.game_scenes.append('Your Choices')
        self.current_graph = None
        self.game_scene_var = tk.StringVar()

        self.init_frame_config()
        # self.frame_config.grid_forget()

        self.robots_pos = {
            'D2_1': None,
            'D2_2': None,
            'Q5_1': None,
            'Q5_2': None,
        }

        self.flags_pos = {
            'flag_D2': None,
            'flag_Q5': None
        }

    def load_scenes(self):
        scenes = []
        dp = os.path.join(base_dir, 'scenes')
        if not os.path.exists(dp):
            raise FileNotFoundError
        for fn in os.listdir(dp):
            _fn, _ext = os.path.splitext(fn)
            if _fn == '.DS_Store':
                continue
            print(_fn)
            print(_fn.split('_'))
            _, size, _ = _fn.split('_')
            r, c = size.split('x')
            r = int(r)
            c = int(c)
            if _ext.lower() == '.sc':
                fp = os.path.join(dp, fn)
                with open(fp, 'rb') as f:
                    _ = pickle.load(f)
                    scenes.append(
                        (_fn, _, r, c)
                        )
        scenes.sort()
        return scenes

    def switch_to_config_frame(self):
        print('switch')
        if 'frame_work' in self.__dict__:
            self.frame_work.destroy()

        self.init_frame_config()

    def init_frame_config(self):
        self.frame_config = tk.Frame(self, bg='white', width=300, height=400)
        self.frame_config.grid(row=0, column=0, sticky='news')
        self.frame_config.rowconfigure(0, weight=1)
        self.frame_config.rowconfigure(7, weight=1)

        self.frame_config.columnconfigure(0, weight=1)
        self.frame_config.columnconfigure(1, weight=1)
        self.frame_config.columnconfigure(2, weight=1)
        self.frame_config.columnconfigure(3, weight=1)

        tk.Label(
            self.frame_config, text='System Config', justify='center', bg='white',
            font=("Helvetica", 16, 'bold')

                 ).grid(
            row=1, column=1, columnspan=2
        )

        tk.Label(self.frame_config, text='Game Scene:', anchor='e', bg='white').grid(
            row=2, column=1, sticky='e',
            pady=10)

        self.comb_scene = tk.ttk.Combobox(
            master=self.frame_config,
            textvariable=self.game_scene_var,
            values=self.game_scenes,
            # postcommand=self.change_scene_choice
            )
        self.comb_scene.bind("<<ComboboxSelected>>", self.change_scene_choice)
        self.comb_scene.grid(row=2, column=2, sticky='w', padx=10, pady=10)

        tk.Label(self.frame_config, text='Row Number:', anchor='e', bg='white').grid(
            row=3, column=1, sticky='e', pady=10
        )

        self.entry_rows = tk.Entry(self.frame_config, textvariable=self.rows_var,)
        self.entry_rows.grid(
            row=3, column=2, sticky='w', padx=10, pady=10
        )

        tk.Label(self.frame_config, text='Col Number:', anchor='e', bg='white').grid(
            row=4, column=1, sticky='e', pady=10
        )

        self.entry_cols = tk.Entry(self.frame_config, textvariable=self.cols_var, )
        self.entry_cols.grid(
            row=4, column=2, sticky='w', padx=10, pady=10
        )

        tk.Label(self.frame_config, text='First Player:', anchor='e', bg='white').grid(
            row=5, column=1, sticky='e', pady=10
        )

        self.comb_first_player = tk.ttk.Combobox(
            master=self.frame_config,
            textvariable=self.first_var,
            values=[
                'D2',
                'Q5',
                'Random'
            ]
        )
        self.comb_first_player.grid(
            row=5, column=2, sticky='w', padx=10, pady=10
        )
        self.comb_first_player.current(0)

        tk.Button(
            self.frame_config, text='Confirm', bg='white', command=self.switch_to_frame_work
                  ).grid(
            row=6, column=1, columnspan=2, pady=10,
            # sticky='ew'
        )

        self.comb_scene.current(0)
        self.change_scene_choice()

    def change_scene_choice(self, event=None):
        ''''''
        choice = self.game_scene_var.get()
        index = self.game_scenes.index(choice)
        if index == len(self.graph_table):
            r = c = ''
            self.current_graph = None
            self.entry_rows.configure(state=tk.NORMAL)
            self.entry_cols.configure(state=tk.NORMAL)
            self.rows_var.set(r)
            self.cols_var.set(c)
        else:
            _, self.current_graph, r, c = self.graph_table[index]
            self.rows_var.set(r)
            self.cols_var.set(c)
            self.entry_rows.configure(state=tk.DISABLED)
            self.entry_cols.configure(state=tk.DISABLED)

    def init_frame_work(self):
        if 'frame_work' in self.__dict__:
            self.frame_work.destroy()
        if 'frame_config' in self.__dict__:
            self.frame_config.destroy()

        self.frame_work = PlayGround(
            master=self, cols=self.cols,
            rows=self.rows, first=self.first,
            graph=self.current_graph)
        self.current_graph.robots_pos = copy.deepcopy(self.robots_pos)
        self.current_graph.flags_pos = copy.deepcopy(self.flags_pos)
        self.frame_work.grid(row=0, column=0, sticky='news')

    def switch_to_frame_work(self):
        rows = self.cols_var.get()
        cols = self.cols_var.get()
        if rows == '':
            rows = 0
        else:
            rows = int(rows)

        if cols == '':
            cols = 0
        else:
            cols = int(cols)
        if rows < 2 or cols < 2:
            return self.show_warning_message(
                message='the Number of both Rows and Cols must be supplied and bigger than 2.')

        self.rows = rows
        self.cols = cols
        self.first = self.first_var.get()
        if self.first == 'Random':
            self.first = random.choice(['D2', 'Q5'])

        if self.current_graph is None:
            vertics, edges = generate_random(self.rows, self.cols)

            self.current_graph = Graph(
                V=vertics, E=edges,
                robots_pos=copy.deepcopy(self.robots_pos),
                flags_pos=copy.deepcopy(self.flags_pos))

        self.frame_config.grid_forget()
        self.init_frame_work()


    def show_warning_message(self, message, title='Warning'):
        return tk.messagebox.showwarning(message=message, title=title)

    def show_info_message(self, message, title='Info'):
        return tk.messagebox.showinfo(message=message, title=title)

    def show_error_message(self, message, title='Error'):
        return tk.messagebox.showerror(message=message, title=title)

class PlayGround(tk.Frame):
    def __init__(self, rows, cols, first, graph,  master=None, root=None):
        super().__init__(master=master)
        if not isinstance(rows, int):
            raise TypeError
        if not isinstance(cols, int):
            raise TypeError
        if rows < 2:
            raise ValueError
        if rows < 2:
            raise ValueError

        if not isinstance(first, str):
            raise TypeError

        if not isinstance(graph, Graph):
            raise TypeError

        self.root = root

        if first not in ['D2', 'Q5']:
            raise ValueError

        self.first = first
        self.second = {'D2', 'Q5'} - {self.first}
        self.second = list(self.second)[0]
        self.current_team = None
        self.round = None
        self.current_sn = None

        print(rows, cols, self.first, self.second)

        self.q = queue.Queue()
        self.setup_ui()

        self.graph = graph
        self.board = Board(master=self, rows=rows, cols=cols, graph=self.graph, q=self.q)
        self.board.grid(row=0, column=0, sticky='news')
        self.board.draw_scene()

        self.stages = (
            'init_flags_first',
            'init_flags_second',
            'init_players_first_1',
            'init_players_first_2',
            'init_players_second_1',
            'init_players_second_2',
            'play_game'
        )

        self.scripts = list(self.stages)

        t = threading.Thread(target=self.game_service)
        t.setDaemon(True)
        t.start()

        self.arrow_key = 0

    def setup_ui(self):
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        right_area = tk.Frame(self)
        right_area.grid(row=0, column=1, sticky='news')

        right_area.columnconfigure(0, weight=1)
        right_area.rowconfigure(0, weight=1)
        right_area.rowconfigure(4, weight=1)
        self.hint_var = tk.StringVar(
            value='Please click in one of grids in \nleft board to Put {}\'s flag.'.format(
                self.first))
        self.label_hint = tk.Label(master=right_area, textvariable=self.hint_var, justify='left')
        self.label_hint.grid(
            row=1, column=0, sticky='news', padx=10, pady=20
        )
        self.y_bar = tk.Scrollbar(right_area, orient=tk.VERTICAL)
        self.y_bar.grid(
            row=2, column=1, sticky='ns'
        )

        self.history_area = tk.Text(
            master=right_area, yscrollcommand=self.y_bar.set, width=30, height=8, state='disabled'
        )
        self.history_area.grid(
            row=2, column=0, sticky='news',
        )

        self.y_bar.configure(command=self.history_area.yview)

        tk.Button(
            master=right_area, text='Clear',
            command=self.master.init_frame_work
        ).grid(
            row=3, column=0, columnspan=2, pady=20
        )

    def get_stage(self):
        return self.scripts[0]

    def finish_stage(self, stage):
        if stage not in self.stages:
            raise ValueError
        if stage != 'play_game' and stage == self.get_stage():
            self.scripts.remove(stage)

        side, name = self.parse_stage()
        if side == 'flags':
            self.hint_var.set(
                'Please click in one of grids in \nleft board to Put {}\'s flag.'.format(
                    name)
            )
        elif side == 'players':
            self.hint_var.set(
                'Please click in one of grids in \nleft board to Put robot {}'.format(
                    name)
            )
        elif side == 'game':
            self.hint_var.set(
                '{}\'s turn. Please type 1-9 or arrow keys'.format(name)
            )

    def game_service(self):
        self.board.can_edit = True
        while True:
            if not self.q.empty():
                p = self.q.get()
                stage = self.get_stage()
                side, name = self.parse_stage()
                if self.board.can_edit is True:
                    self.board.unbind("<Button-1>")
                if side == 'flags':
                    self.board.draw_flags(row_col=p, tag_aft=name)
                    self.log_operations(message='Put {}\'s flag at {}'.format(name, p))
                    self.finish_stage(stage=stage)
                elif side == 'players':
                    self.board.draw_robot(row_col=p, tag_aft=name)
                    self.log_operations(message='Put robot {} at {}'.format(name, p))
                    self.finish_stage(stage=stage)
                    if name == '{}_2'.format(self.second):
                        self.board.can_edit = False
                        # self.board.unbind("<Button-1>")
                        self.master.bind('<Key>', self.key_pressed)
                        self.current_team = self.first
                        self.round = 1
                        self.log_operations(message='all done.')
                        self.log_operations(message='Round {}'.format(self.round))
                        self.log_operations(message='{}\'s Turn:'.format(self.current_team))
                        self.current_sn = 1
                else:
                    self.master.unbind('<Key>')
                    robot_1 = '{}_1'.format(self.current_team)
                    robot_2 = '{}_2'.format(self.current_team)

                    if self.arrow_key == 0 and isinstance(p, int):
                    # if isinstance(p, int):
                        t = True if self.current_team == 'D2' else False
                        print(self.current_team, t)
                        moves = self.graph.get_best_move(D2=t, limit=p)
                        print(moves)
                        moves = moves[0]
                        if not isinstance(moves, dict):
                            move_1 = move_2 = 'stay'
                        else:
                            move_1 = moves[robot_1]
                            move_2 = moves[robot_2]
                    elif self.arrow_key >= 0 and isinstance(p, str):
                        if self.current_sn == 1:
                            move_1 = p
                            move_2 = None
                        elif self.current_sn == 2:
                            move_1 = None
                            move_2 = p
                        else:
                            raise ValueError
                    else:
                        print(self.arrow_key, p)
                        raise ValueError

                    if isinstance(move_1, str):
                        self.graph.perform_move(robot_1, move_1)
                        self.board.update_robot(name=robot_1)
                        self.log_operations(message='Move Robot {} {}'.format(robot_1, move_1))
                        if self.graph.game_over() is True:
                            self.hint_var.set('{} Win!'.format(self.current_team))
                            return self.master.show_info_message(message='{} Win!'.format(self.current_team),
                                                                 title='Game Over')
                        self.current_sn += 1

                    if isinstance(move_2, str):
                        self.graph.perform_move(robot_2, move_2)
                        self.board.update_robot(name=robot_2)
                        self.log_operations(message='Move Robot {} {}'.format(robot_2, move_2))
                        if self.graph.game_over() is True:
                            self.hint_var.set('{} Win!'.format(self.current_team))
                            return self.master.show_info_message(message='{} Win!'.format(self.current_team),
                                                                 title='Game Over')
                        self.current_sn += 1

                    self.next_round()
                    self.master.bind('<Key>', self.key_pressed)
                if self.board.can_edit is True:
                    self.board.bind("<Button-1>", self.board.left_click)

            time.sleep(0.1)

    def next_round(self):
        if self.current_sn == 3:
            if self.current_team == self.second:
                self.round += 1
                self.current_team = self.first
                self.current_sn = 1
                self.log_operations(message='Round {}'.format(self.round))
                self.log_operations(message='{}\'s Turn:'.format(self.current_team))
                self.hint_var.set('{}\'s turn. Please type 1-9 or arrow keys'.format(self.current_team))
                self.arrow_key = 0

            elif self.current_team == self.first:
                self.current_team = self.second
                self.log_operations(message='{}\'s Turn:'.format(self.current_team))
                self.hint_var.set('{}\'s turn. Please type 1-9 or arrow keys'.format(self.current_team))

            self.current_sn = 1

    def parse_stage(self):
        stage = self.get_stage()
        stage = stage.split('_')
        if stage[1] == 'flags':
            return 'flags', self.__dict__[stage[-1]]
        elif stage[1] == 'players':
            return 'players', '{}_{}'.format(self.__dict__[stage[2]], stage[-1])
        else:
            if self.current_team is None:
                return 'game', self.first
            next_team = {'D2', 'Q5'} - {self.current_team}
            next_team = list(next_team)[0]
            return 'game', next_team

    def log_operations(self, message):
        self.history_area.configure(state=tk.NORMAL)
        self.history_area.insert(tk.END, '\n')
        self.history_area.insert(tk.END, message)
        self.history_area.insert(tk.END, '\n')
        self.history_area.configure(state=tk.DISABLED)
        self.history_area.yview('end')

    def key_pressed(self, event):
        print('pressed', event.keysym, '"{}"'.format(event.char))

        k = event.keysym
        news = ['Up', 'Down', 'Left', 'Right']
        directions = ['north', 'south', 'west', 'east']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if self.arrow_key == 2:
            self.arrow_key = 0

        if k in news:
            self.arrow_key += 1
            if self.arrow_key == 3:
                self.arrow_key = 0
            self.q.put(directions[news.index(k)])
        elif self.arrow_key == 0:
            try:
                if k[-2] == '_':
                    k = k[-1]
            except IndexError:
                pass
            if k in numbers:
                k = int(k)
                self.q.put(k)


if __name__ == '__main__':

    app = MainGuiApp()
    app.mainloop()





