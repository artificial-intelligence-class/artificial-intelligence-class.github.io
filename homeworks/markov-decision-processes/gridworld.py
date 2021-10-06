import argparse
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

    def __init__(self, noise: float, living_reward: float, grid: Tuple[Tuple[Any, ...], ...]):
        self.__noise = noise
        self.__living_reward = living_reward
        self.__n = len(grid)
        self.__m = len(grid[0])
        self.__grid = grid
        self.__states = {(x, y) for x in range(self.__n) for y in range(self.__m) if
                         grid[x][y] in (' ', 'S')}

    @property
    def states(self) -> Set[State]:
        return self.__states

    def get_actions(self, state: State) -> Set[Action]:
        x, y = state
        if x < 0 or x >= self.__n or y < 0 or y >= self.__m:
            raise ValueError('not a valid state')
        if isinstance(self.__grid[state[0]][state[1]], float):  # terminal
            return set()
        return {*Gridworld.Action}

    def _do_action(self, state: State, action: Action) -> State:
        x, y = state

        if action == Gridworld.Action.Up:
            target_x, target_y = x - 1, y
        elif action == Gridworld.Action.Down:
            target_x, target_y = x + 1, y
        elif action == Gridworld.Action.Left:
            target_x, target_y = x, y - 1
        else:
            target_x, target_y = x, y + 1

        if target_x < 0 or target_x >= self.__n or target_y < 0 or target_y >= self.__m or \
                self.__grid[target_x][target_y] == '#':
            return state
        return target_x, target_y

    @lru_cache(maxsize=2)
    def get_transitions(self, current_state: State, action: Action) -> Dict[State, float]:
        if action not in self.get_actions(current_state):
            raise ValueError('not a valid action')

        if self.__noise <= 0.:
            return {self._do_action(current_state, action): 1.}

        remaining = self.__noise / 2.
        if action in (Gridworld.Action.Up, Gridworld.Action.Down):
            outcomes = (
                (self._do_action(current_state, action), 1 - self.__noise),
                (self._do_action(current_state, Gridworld.Action.Left), remaining),
                (self._do_action(current_state, Gridworld.Action.Right), remaining)
            )
        else:
            outcomes = (
                (self._do_action(current_state, action), 1 - self.__noise),
                (self._do_action(current_state, Gridworld.Action.Up), remaining),
                (self._do_action(current_state, Gridworld.Action.Down), remaining)
            )

        transitions = {}
        for outcome, val in outcomes:
            transitions[outcome] = transitions.get(outcome, 0.) + val
        return transitions

    def get_reward(self, current_state: State, action: Action, next_state: State) -> float:
        if next_state not in self.get_transitions(current_state, action):
            raise ValueError('next state is not reachable from current state')
        grid_value = self.__grid[next_state[0]][next_state[1]]
        return grid_value if isinstance(grid_value, float) else self.__living_reward


class GUI(tk.Tk):
    SQUARE_SIZE = 100

    def __init__(self, agent, grid, init_iter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__grid = grid
        self.__rows = len(grid)
        self.__cols = len(grid[0])
        self.__agent = agent
        self.__iter_backup = []
        self.__cache_agent()

        width, height = GUI.SQUARE_SIZE * self.__cols, GUI.SQUARE_SIZE * self.__rows

        tk.Label(self, text=agent.__class__.__name__).pack(side=tk.TOP)

        frame = tk.LabelFrame(self, text='Display type')

        self.__display_type = tk.IntVar(frame, value=0)
        self.__display_type.trace_add('write', self.__display_mode_changed)

        tk.Radiobutton(frame, text='None', variable=self.__display_type,
                       value=0).grid(row=0, column=0)
        tk.Radiobutton(frame, text='V*(s)', variable=self.__display_type,
                       value=1).grid(row=0, column=1)
        tk.Radiobutton(frame, text='Q*(s,a)', variable=self.__display_type,
                       value=2).grid(row=0, column=2)
        tk.Radiobutton(frame, text='π*(s)', variable=self.__display_type,
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

        tk.Spinbox(frame, from_=0, increment=1, to=100,
                   textvariable=self.__iteration).grid(row=0, column=1)
        frame.pack(side=tk.TOP)

        self.title('Gridworld - CIS 521')
        self.__draw_grid()

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
        backup = self.__iter_backup[self.__iteration.get()]
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                self.__canvas.create_text(
                    (j + .5) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    text=format(backup[i, j][0], '.2f'),
                    font=font, tags='display')

    def __draw_q_values(self):
        font = tk_font.Font(size=self.SQUARE_SIZE // 10)
        backup = self.__iter_backup[self.__iteration.get()]
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                q_values = backup[i, j][1]
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
        backup = self.__iter_backup[self.__iteration.get()]
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

    def __display_mode_changed(self, *_):
        self.__canvas.delete('display')
        typ = self.__display_type.get()
        if typ == 1:
            self.__draw_values()
        elif typ == 2:
            self.__draw_q_values()
        elif typ == 3:
            self.__draw_policy()

    def __cache_agent(self):
        cache = dict()
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                cache[i, j] = (
                    self.__agent.get_value((i, j)),
                    dict(((a, self.__agent.get_q_value((i, j), a)) for a in Gridworld.Action)),
                    self.__agent.get_best_policy((i, j))
                )
        self.__iter_backup.append(cache)

    def __iteration_changed(self, *_):
        try:
            it = self.__iteration.get()
        except tk.TclError:
            return
        if it >= len(self.__iter_backup):
            for __ in range(it - len(self.__iter_backup) + 1):
                self.__agent.iterate()
                self.__cache_agent()
        self.__display_mode_changed()


PRESET_GRIDS = {
    'book': (
        (' ', ' ', ' ', 1.),
        (' ', '#', ' ', -1.),
        (' ', ' ', ' ', 'S'),
    ),
    'bridge': (
        ('#', -100., -100., -100., -100., -100., '#'),
        (1., 'S', ' ', ' ', ' ', ' ', 10.),
        ('#', -100., -100., -100., -100., -100., '#'),
    ),
    'discount': (
        (' ', ' ', ' ', ' ', ' '),
        (' ', '#', ' ', ' ', ' '),
        (' ', '#', 1., '#', 10.),
        ('S', ' ', ' ', ' ', ' '),
        (-10., -10., -10., -10., -10.),
    ),
    'maze': (
        (' ', ' ', ' ', 1.),
        ('#', '#', ' ', '#'),
        (' ', '#', ' ', ' '),
        (' ', '#', '#', ' '),
        ('S', ' ', ' ', ' '),
    )
}


def main():
    def argtype(arg):
        """ Type function for argparse - a float within some predefined bounds """
        try:
            f = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be a floating point number')
        if 0 <= f <= 1:
            return f
        raise argparse.ArgumentTypeError('must be a real number between 0 and 1')

    parser = argparse.ArgumentParser(
        description='Gridworld GUI, CIS 521, Artificial Intelligence',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('grid', metavar='GRID_NAME', help='grid preset', nargs='?',
                        choices=PRESET_GRIDS.keys(), default='book')
    parser.add_argument('-a', '--agent', help='iteration agent type',
                        choices=('value', 'policy'), default='value')
    parser.add_argument('-d', '--discount', help='discount factor gamma (γ)',
                        type=argtype, default=0.9)
    parser.add_argument('-n', '--noise', help='probability of a noisy outcome for an action',
                        type=argtype, default=0.2)
    parser.add_argument('-l', '--living-reward', help='living reward for every non-terminal state',
                        type=float, default=0.)
    parser.add_argument('-i', '--iteration', help='initial iteration to display',
                        type=int, default=0)
    args = parser.parse_args()
    grid = PRESET_GRIDS[args.grid]
    game = Gridworld(noise=args.noise, living_reward=args.living_reward, grid=grid)
    agent = getattr(agents, args.agent.title() + 'IterationAgent')(game, discount=args.discount)
    GUI(agent, grid, args.iteration).mainloop()


if __name__ == '__main__':
    main()
