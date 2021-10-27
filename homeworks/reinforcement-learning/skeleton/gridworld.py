import argparse
import random
import time
import tkinter as tk
import tkinter.font as tk_font
from enum import Enum, auto
from functools import lru_cache
from typing import *

import agents


class Gridworld:
    State = Tuple[int, int]

    class Action(Enum):
        Up = auto()
        Down = auto()
        Left = auto()
        Right = auto()

    def __init__(self, grid: Tuple[Tuple[Any, ...], ...]):
        self.__n = len(grid)
        self.__m = len(grid[0])
        self.__grid = grid

    @lru_cache(maxsize=None)
    def get_actions(self, state: State) -> Set[Action]:
        x, y = state
        if x < 0 or x >= self.__n or y < 0 or y >= self.__m:
            raise ValueError('not a valid state')
        if isinstance(self.__grid[x][y], float):  # terminal
            return set()
        return {*Gridworld.Action}


@lru_cache(maxsize=None)
def get_start_point(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                return i, j


class Environment:
    def __init__(self, agent, noise: float, living_reward: float,
                 grid: Tuple[Tuple[Any, ...], ...]):
        self.__grid = grid
        self.__n = len(grid)
        self.__m = len(grid[0])
        self.__noise = noise
        self.__living_reward = living_reward

        self.agent = agent
        self.position = get_start_point(grid)

    def __do_action(self, action: Gridworld.Action) -> Gridworld.State:
        x, y = self.position

        if action == Gridworld.Action.Up:
            target_x, target_y = x - 1, y
        elif action == Gridworld.Action.Down:
            target_x, target_y = x + 1, y
        elif action == Gridworld.Action.Left:
            target_x, target_y = x, y - 1
        else:
            target_x, target_y = x, y + 1

        if 0 <= target_x < self.__n and 0 <= target_y < self.__m and \
                self.__grid[target_x][target_y] != '#':
            return target_x, target_y
        return x, y

    def __act(self, action: Gridworld.Action):
        if self.__noise <= 0.:
            self.position = self.__do_action(action)
            return

        remaining = self.__noise / 2.
        if action in (Gridworld.Action.Up, Gridworld.Action.Down):
            outcomes = (
                (self.__do_action(action), 1 - self.__noise),
                (self.__do_action(Gridworld.Action.Left), remaining),
                (self.__do_action(Gridworld.Action.Right), remaining)
            )
        else:
            outcomes = (
                (self.__do_action(action), 1 - self.__noise),
                (self.__do_action(Gridworld.Action.Up), remaining),
                (self.__do_action(Gridworld.Action.Down), remaining)
            )

        transitions = {}
        for outcome, val in outcomes:
            transitions[outcome] = transitions.get(outcome, 0.) + val
        options, weights = zip(*transitions.items())
        self.position = random.choices(options, weights)[0]

    def iterate(self, action=None) -> bool:
        if isinstance(self.__grid[self.position[0]][self.position[1]], float):
            self.position = get_start_point(self.__grid)
            return True

        state = self.position
        if action is None:
            action = self.agent.get_action(self.position)
        self.__act(action)
        grid_value = self.__grid[self.position[0]][self.position[1]]
        reward = grid_value if isinstance(grid_value, float) else self.__living_reward
        self.agent.update(state, action, self.position, reward)

        return False


class GUI(tk.Tk):
    SQUARE_SIZE = 100
    ANIMATION_SPEED = 0.1

    def __init__(self, env: Environment, grid, init_iter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__grid = grid
        self.__rows = len(grid)
        self.__cols = len(grid[0])
        self.__env = env
        self.__episode_counter = 1
        self.__iter_backup = []
        self.__cache_env()

        width, height = GUI.SQUARE_SIZE * self.__cols, GUI.SQUARE_SIZE * self.__rows

        tk.Label(self, text=env.agent.__class__.__name__).pack(side=tk.TOP)
        epi_frame = tk.Frame(self)

        self.__episode = tk.Label(epi_frame)
        self.__episode.grid(row=0, column=0)

        tk.Button(epi_frame, text='Run Episode', command=self.__run_episode).grid(row=0, column=1)
        epi_frame.pack(side=tk.TOP)

        frame = tk.LabelFrame(self, text='Display type')

        self.__display_type = tk.IntVar(frame, value=0)
        self.__display_type.trace_add('write', self.__display_mode_changed)

        tk.Radiobutton(frame, text='None', variable=self.__display_type,
                       value=0).grid(row=0, column=0)
        tk.Radiobutton(frame, text='Q(s,a)', variable=self.__display_type,
                       value=1).grid(row=0, column=1)
        tk.Radiobutton(frame, text='V(s)', variable=self.__display_type,
                       value=2).grid(row=0, column=2)
        tk.Radiobutton(frame, text='π(s)', variable=self.__display_type,
                       value=3).grid(row=0, column=3)

        frame.pack(side=tk.BOTTOM)

        self.__canvas = tk.Canvas(
            self, width=width + 1, height=height + 1, highlightthickness=0)

        for i in range(self.__rows + 1):
            self.__canvas.create_line(
                0, i * GUI.SQUARE_SIZE, width, i * GUI.SQUARE_SIZE)
        for i in range(self.__cols + 1):
            self.__canvas.create_line(
                i * GUI.SQUARE_SIZE, 0, i * GUI.SQUARE_SIZE, height)

        frame = tk.Frame(self)
        tk.Label(frame, text='# Iteration: ').grid(row=0, column=0)

        self.__iteration = tk.IntVar(frame, value=len(self.__iter_backup) - 1)
        self.__iteration.trace_add('write', self.__iteration_changed)
        self.__iteration.set(init_iter)

        tk.Spinbox(frame, from_=0, increment=1, to=100000,
                   textvariable=self.__iteration).grid(row=0, column=1)
        frame.pack(side=tk.TOP)

        self.title('Gridworld - CIS 521')
        self.__draw_grid()
        self.__redraw_aux()
        self.__canvas.focus_set()
        self.__canvas.bind('<Key>', self.__pressed_key)
        self.__canvas.bind('<Button-1>', lambda _: self.__canvas.focus_set())

    def __pressed_key(self, event):
        action = getattr(Gridworld.Action, event.keysym, None)
        if action is None:
            return
        cur_view = int(self.__iteration.get())
        cur_iter = len(self.__iter_backup) - 1
        self.__iteration.set(cur_iter)
        if cur_view < cur_iter:
            print('not latest iteration, fast-forward...')
            return
        if self.__env.iterate(action):
            self.__episode_counter += 1
        self.__cache_env()
        self.__iteration.set(cur_iter + 1)
        self.__redraw_aux()
        self.__display_mode_changed()

    def __run_episode(self):
        start_with = self.__iter_backup[self.__iteration.get()][2]
        while self.__iter_backup[self.__iteration.get()][2] == start_with:
            self.__iteration.set(self.__iteration.get() + 1)
            self.__iteration_changed()
            self.update()
            time.sleep(self.ANIMATION_SPEED)

    def __draw_rectangle(self, i, j, **kwargs):
        self.__canvas.create_rectangle(
            j * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
            (j + 1) * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE, kwargs)

    def __draw_grid(self):
        font = tk_font.Font(size=self.SQUARE_SIZE // 6, weight='bold')
        for i in range(self.__rows):
            for j in range(self.__cols):
                cell = self.__grid[i][j]
                if cell == '#':
                    self.__draw_rectangle(i, j, fill='black')
                elif cell == 'S':
                    self.__draw_rectangle(i, j, fill='yellow')
                elif isinstance(cell, float):
                    if cell > 0:
                        self.__draw_rectangle(i, j, fill='green')
                    elif cell < 0:
                        self.__draw_rectangle(i, j, fill='red')
                    self.__canvas.create_text(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        text=format(cell, '.2f'), font=font)
        self.__canvas.pack()

    def __draw_values(self):
        font = tk_font.Font(size=self.SQUARE_SIZE // 6)
        backup = self.__iter_backup[self.__iteration.get()][0]
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                self.__canvas.create_text(
                    (j + .5) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    text=format(backup[i, j][1], '.2f'),
                    font=font, tags='display')

    def __draw_q_values(self):
        font = tk_font.Font(size=self.SQUARE_SIZE // 10)
        backup = self.__iter_backup[self.__iteration.get()][0]
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                q_values = backup[i, j][0]
                self.__canvas.create_line(
                    j * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
                    (j + 1) * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE,
                    tags='display')
                self.__canvas.create_line(
                    (j + 1) * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
                    j * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE,
                    tags='display')
                self.__canvas.create_text(
                    (j + .5) * GUI.SQUARE_SIZE, (i + .15) * GUI.SQUARE_SIZE,
                    text=format(q_values[Gridworld.Action.Up], '.2f'),
                    font=font, tags='display')
                self.__canvas.create_text(
                    (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    text=format(q_values[Gridworld.Action.Left], '.2f'),
                    font=font, tags='display')
                self.__canvas.create_text(
                    (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    text=format(q_values[Gridworld.Action.Right], '.2f'),
                    font=font, tags='display')
                self.__canvas.create_text(
                    (j + .5) * GUI.SQUARE_SIZE, (i + .85) * GUI.SQUARE_SIZE,
                    text=format(q_values[Gridworld.Action.Down], '.2f'),
                    font=font, tags='display')

    def __draw_policy(self):
        options = {
            'width': GUI.SQUARE_SIZE // 10,
            'arrow': tk.FIRST,
            'arrowshape': (GUI.SQUARE_SIZE // 5, GUI.SQUARE_SIZE // 5, GUI.SQUARE_SIZE // 10),
            'tags': 'display'
        }
        backup = self.__iter_backup[self.__iteration.get()][0]
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                policy = backup[i, j][2]
                if policy == Gridworld.Action.Up:
                    self.__canvas.create_line(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .2) * GUI.SQUARE_SIZE,
                        (j + .5) * GUI.SQUARE_SIZE, (i + .8) * GUI.SQUARE_SIZE,
                        **options)
                elif policy == Gridworld.Action.Down:
                    self.__canvas.create_line(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .8) * GUI.SQUARE_SIZE,
                        (j + .5) * GUI.SQUARE_SIZE, (i + .2) * GUI.SQUARE_SIZE,
                        **options)
                elif policy == Gridworld.Action.Right:
                    self.__canvas.create_line(
                        (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        **options)
                elif policy == Gridworld.Action.Left:
                    self.__canvas.create_line(
                        (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        **options)

    def __redraw_aux(self):
        (x, y), epi = self.__iter_backup[self.__iteration.get()][1:]
        self.__episode.configure(text='# Episode: %d' % epi)
        self.__canvas.delete('agent')
        self.__canvas.create_oval((y + .4) * GUI.SQUARE_SIZE, (x + .4) * GUI.SQUARE_SIZE,
                                  (y + .6) * GUI.SQUARE_SIZE, (x + .6) * GUI.SQUARE_SIZE,
                                  tags='agent', fill='cyan')

    def __display_mode_changed(self, *_):
        self.__canvas.delete('display')
        typ = self.__display_type.get()
        if typ == 1:
            self.__draw_q_values()
        elif typ == 2:
            self.__draw_values()
        elif typ == 3:
            self.__draw_policy()

    def __cache_env(self):
        cache = dict()
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                cache[i, j] = (
                    dict(((a, self.__env.agent.get_q_value((i, j), a)) for a in Gridworld.Action)),
                    self.__env.agent.get_value((i, j)),
                    self.__env.agent.get_best_policy((i, j)),
                )
        self.__iter_backup.append((
            cache,
            self.__env.position,
            self.__episode_counter))

    def __iteration_changed(self, *_):
        try:
            it = self.__iteration.get()
        except tk.TclError:
            return
        if it >= len(self.__iter_backup):
            for __ in range(it - len(self.__iter_backup) + 1):
                if self.__env.iterate():
                    self.__episode_counter += 1
                self.__cache_env()
        self.__redraw_aux()
        self.__display_mode_changed()


PRESET_GRIDS = {
    'book': (
        (' ', ' ', ' ', 1.),
        (' ', '#', ' ', -1.),
        ('S', ' ', ' ', ' '),
    ),
    'bridge': (
        ('#', -100., -100., -100., -100., -100., '#'),
        (1., 'S', ' ', ' ', ' ', ' ', 10.),
        ('#', -100., -100., -100., -100., -100., '#'),
    ),
}


def main():
    def argtype(arg):
        try:
            f = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be a floating point number')
        if 0 <= f <= 1:
            return f
        raise argparse.ArgumentTypeError('must be a real number between 0 and 1')

    parser = argparse.ArgumentParser(
        description='Gridworld GUI for QAgent, CIS 521, Artificial Intelligence',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('grid', metavar='GRID_NAME', help='grid preset', nargs='?',
                        choices=PRESET_GRIDS.keys(), default='book')
    parser.add_argument('-d', '--discount', help='discount factor gamma (γ)',
                        type=argtype, default=0.9)
    parser.add_argument('-n', '--noise', help='probability of a noisy outcome for an action',
                        type=argtype, default=0.2)
    parser.add_argument('-l', '--living-reward', help='living reward for every non-terminal state',
                        type=float, default=0.)
    parser.add_argument('-r', '--learning-rate', help='learning reward for Q agent',
                        type=float, default=0.5)
    parser.add_argument('-e', '--epsilon', help='exploration probability for Q agent (ε)',
                        type=float, default=0.3)
    parser.add_argument('-i', '--iteration', help='initial iteration to train',
                        type=int, default=0)
    args = parser.parse_args()
    grid = PRESET_GRIDS[args.grid]
    game = Gridworld(grid)
    agent = agents.QLearningAgent(game, args.discount, args.learning_rate, args.epsilon)
    env = Environment(agent, args.noise, args.living_reward, grid)
    GUI(env, grid, args.iteration).mainloop()


if __name__ == '__main__':
    main()
