import random
import tkinter as tk
import sys
from abc import ABC
from collections import defaultdict
from enum import Enum, auto
from typing import Tuple, Optional, Set

student_name = 'Type your full name here.'


Location = Tuple[int, int]


class Action(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SHOOT = auto()


class R2Droid:
    def __init__(self, rows: int, cols: int, location: Location, shots: int):
        ...  # TODO

    def copy(self):
        ...  # TODO

    def move_location(self, move: Action):
        ...  # TODO

    def shoot(self, other: 'R2Droid', move: Action) -> bool:
        ...  # TODO

    def available_actions(self) -> Set[Action]:
        ...  # TODO


class Agent(ABC):
    """Agent Abstract Base Class, do not modify."""

    def get_best_move(self, self_droid: R2Droid, adv_droid: R2Droid, score_change: int, training: bool) -> Action:
        ...

    def clear(self):
        ...


class QAgent(Agent):
    def __init__(self):
        ...  # TODO

    def get_best_move(self, self_droid: R2Droid, adv_droid: R2Droid, score_change: int, training: bool) -> Action:
        ...  # TODO

    def clear(self):
        ...  # TODO


class MinimaxAgent(Agent):
    def __init__(self):
        ...  # TODO

    def get_best_move(self, self_droid: R2Droid, adv_droid: R2Droid, score_change: int, training: bool) -> Action:
        ...  # TODO

    def clear(self):
        ...  # TODO


###
# You don't have to change anything below
###

class KeyboardAgent(Agent):
    def __init__(self):
        self.__move = None

    def get_best_move(self, *_):
        return self.__move

    def set_move(self, move):
        self.__move = move


SQUARE_SIZE = 50

D2_IMG = '''R0lGODlhJQAxAMQfANXWyMXGuLKzpePk2BpIi9nbzf39/UlSWbWxFcvMvqmpm+jp3czSzoqMg0dq
lae0vt3f0/T08dPZ1JCjusHBsrnBw26Jp+7v6rq7rp2dkcPKyNDRw2xzbJGcpM7W3P///yH5BAEA
AB8ALAAAAAAlADEAAAX/4CeO5GhEg1R5kLdERinPsrFMHWYR2uM4lskgRiuaFozHZGJ5XDyW3+8R
MRYNA8hgwb1EvBeIZMxgVK0lLGStZa8l4jGkTESLLmO4O08ulzUQdVYGEgx8h35+GosagkYGZYd9
iQyLFZcXdh8XhnlvZBoCGBp/ARgYA5oVBA6dS0sPDAocHAIdt1EOjWgGDwQEnQ4IHKyyBxwdvw6/
BA+OMwYTrGseHAgIxRUKAr6szM680g4VpFKsAIUMFVLLDhPPNRUWuez19gcOHTA0BicXXFyy/Ln0
oGDBU6dEbQAw4MIzGxFQDNiygGLAiWsKFACQIAEFCgEYLsiUBuCWBAES/2zo2DFAgI8JRSnIoCBA
gYCObLBZEJICAJAvKcQUQJQCTQU+1wBwFAECgKcDEgzwSWFilowaCwjNIAApAAgFEjDdCGDDALMY
fla0ilUrBq41C4AVWyICWbNoAQQwiREsBFNwbYIN4OjC3bNTf6pkiTKoAKNdBRcgXPewWapETynY
LOAo5LhzmYJ9uuDyz7JCU2IguuFUYLkcx5a9mXcvTww3AzweALgrhYUoC5OFUDrxXt64pz6GsNV3
SL3CNW65vOG4qZsUkDJ/6/s39BKGpRcPUL2i0AJTtTdHKiDBz8Jg0S+QGtJ68uwU/nJn754yiTDi
SeWTbaYQp1tVvWVAQf973/0X33Qe6dWRUCCJYqFRDSjIoH8jACgXGxpxpFJ1IHn0UQAz8ddgh6Mt
oMAxGZT1VEcbVIdBSi919Vh71cG3kYu/cDBaViGu9FICAnCgYUgJnCECFguAtQAGBxzQwE8YNCCA
BLR0AAAHDSDVAJhCbUBWHQZosdEA3VigFwUHZJDAMQ1sYKVrcQoFwEYUoJkRQwl0YEEHrWGgJANV
1gmmAhhkt1paG9H1pFI3XVQWjW/i+FJKep2y50IkpLnRTVmQtWdWIGZV1qYYbDBaHWHU2AZZH8YX
4lNPbZBahGtIqtNGs166kEZtbbQSYwGwsQERKIzmqlMrgUTiR9SeiOt9SmYpFYhEo7kHrUeuFhDt
ajp+dZcWE01GHEYDiKvSpUmBmKtLs5rJ1l9VWTUArii1dCqRIa7rFENbgBWVAPo6FSJj7gGcVV9t
EGdwdQWbWmS0IRH5FKkJZ7TGSmGUVePINTJ2alsUbdEuwAv1E9EXF8Qs88w0zxxQsWVFEAIAOw=='''

Q5_IMG = '''R0lGODlhJQAxAMQfAN9vCktMUDAxNK96Qurq6a+wro+Oi21vcNfZ16FVExAPFJULDMzLx1dYWnNp
Xzo5OUFCRWhILb+achgYHXZ5e19hZCEiJoSDgKiop6CgnyoqLZaXl7y9uysaE////////yH5BAEA
AB8ALAAAAAAlADEAAAX/4CeO5OghDFdgWYF4XinP8rlRVRBATe9ghBhtKPIQMo5Ko2LIYA4B34Uj
JM4Il8ADAjmoMJRo47C5FKpW0wWi0Qge8O0WAj9cLgy01VMIWCZvDQYXYUoCGg9jFwZ6RB4HGhOI
AgYbDwc5WmKKDGkjCBATFm8HBAiXXAEaOlEVFBiNM3wPArWXBBxQE2y7EDoVZLE1G1x0tD07WhAY
BRW+YwYEnh4GtAJLrMUBBggIG8AVFxvSadQPmhoNARMKCwsRARsZORXA49MGOgJaOX/uDRYUWGjl
agOCaRIGDIgQwUGDCOp0NNDQYZ+Dixck5IFBw0iGhwlCihxJMoHCAQYo/zgIVsOOgVoCLMj8o6Cm
TQUaUo3JQcvCwRKnekDYN7SNhpl//uyTCIXN0QIyOAwdCOeN1aNG2yxdQmGoqAkb0HjAMHGCJFoP
NEQAACAk27fwehxgo8DsBbEbApq1gBZRgrZ/4UocQ7cmIxIeMtgUhbYWIjgRDsEZ3FWDzbuIL9zk
+0bt289sI/BoEMayYbwB6+bs/CBC4LYM4YkJE9NNhhJ8dHDZwvqQ2d+j1CnBsQkq4gI8oli19nun
m5xLSEPp0cC4CeRvVDX+I+nCgQOHLPAYHgaZ9SIYUg1NW6vBIQ3ewR8dT7rrA5kYZCiuO2roG2L3
RWfBUYn0QMEa7CiQX/8Jiv0mgH8PGDDVIheMIh51B0Kg14Ik7FfXg7VAQMwbCBjAQVoXGrhGQBZw
OAIGi60SwIMjPlAiB+GNRtqKdd1WAgYJDqTFKhtoYQEhFIyyzxIHUNCVXj6SUECQJ824gwC/mdVa
ArMVcIBeG8gAZE0WDADAAAC5MWBSE6wFQARMXIBAhYAcIBYmASokAWnyPNABHB0w9OA2HGTAAAV7
BdCJCb5E8oAEbAUwBQEBdNDEA20JaaihFNQFyHkerFNTOhkxwQEoHSwiQEjiBfCKOACZpQEHiLnH
Di1uLAGMMsZswcoOvghA5qIiEEDLjDFNNVOB1A35Rxu9sGMBrSOcOKDIV7sEUNMu1PWQg7QQ1LTP
UUcKQY1jDWhYEy1kFlNVoqY9KIoFFZjrTEwPprYLrllp9WC468JxVAAveMDBleQmCEgkWWY5oLBk
CszXOBxImMh9NCmQ700cT8Duts+1IWcGFMDRAIrcwZEgxzVBUIFvMiFi1AEpnLyDVkd9JdO2HDt2
nyg5zdSACr6w8TC5y67s6QRJmtUZtKJAUAADO2yb5RvGIDUgIshe08BvNlnACAZKdAuMHRgwgAAB
bLfNNgqFeueQtw7IGQIAOw=='''


class GUI(tk.Tk):
    def __init__(self, r2_agent, q5_agent, *args, **kwargs):
        self.__rows, self.__cols = 4, 4
        self.__time_remaining = 50
        self.__D2 = r2_agent()
        self.__Q5 = q5_agent()

        super().__init__(*args, **kwargs)
        width, height = SQUARE_SIZE * self.__cols, SQUARE_SIZE * self.__rows

        self.__D2_label = tk.Label(self)
        self.__Q5_label = tk.Label(self)

        self.__D2_label.pack(side=tk.LEFT, padx=5)
        self.__Q5_label.pack(side=tk.RIGHT, padx=5)

        self.__D2_image = tk.PhotoImage(data=D2_IMG)
        self.__Q5_image = tk.PhotoImage(data=Q5_IMG)

        self.__time_label = tk.Label(self)
        self.__time_label.pack(side=tk.TOP)

        self.__status_label = tk.Label(self)
        self.__status_label.pack(side=tk.BOTTOM)

        self.__canvas = tk.Canvas(
            self, bg='grey', width=width + 1, height=height + 1, highlightthickness=0)
        for i in range(self.__rows + 1):
            self.__canvas.create_line(
                0, i * SQUARE_SIZE, width, i * SQUARE_SIZE)
        for i in range(self.__cols + 1):
            self.__canvas.create_line(
                i * SQUARE_SIZE, 0, i * SQUARE_SIZE, height)

        self.reset()
        self.__canvas.pack(side=tk.BOTTOM)
        self.bind('<Key>', self.__key_press)

    def __key_press(self, event):
        if not isinstance(self.__D2, KeyboardAgent):
            if event.keysym == 'space':
                self.run_episode()
            return
        mapping = {
            'space': Action.SHOOT,
            'Up': Action.MOVE_UP,
            'Down': Action.MOVE_DOWN,
            'Left': Action.MOVE_LEFT,
            'Right': Action.MOVE_RIGHT
        }
        if event.keysym in mapping:
            action = mapping[event.keysym]
            if action in self.__D2_droid.available_actions():
                self.__D2.set_move(mapping[event.keysym])
                self.run_episode()

    def __update_location(self):
        self.__canvas.delete('r2')
        x, y = self.__D2_droid.location
        self.__canvas.create_image(
            (y + .5) * SQUARE_SIZE, (x + .5) * SQUARE_SIZE, image=self.__D2_image, tags='r2')
        x, y = self.__Q5_droid.location
        self.__canvas.create_image(
            (y + .5) * SQUARE_SIZE, (x + .5) * SQUARE_SIZE, image=self.__Q5_image, tags='r2')

    def __display_laser(self, start, move, color):
        if move == Action.SHOOT:
            self.__canvas.create_line(
                0, (start[0] + .5) * SQUARE_SIZE, self.__cols * SQUARE_SIZE, (start[0] + .5) * SQUARE_SIZE, fill=color,
                tags='r2', width=5, stipple='gray50')
            self.__canvas.create_line(
                (start[1] + .5) * SQUARE_SIZE, 0, (start[1] + .5) * SQUARE_SIZE, self.__rows * SQUARE_SIZE, fill=color,
                tags='r2', width=5, stipple='gray50')

    def __is_game_over(self):
        return self.__time_remaining <= 0 or (self.__D2_droid.shots <= 0 and self.__Q5_droid.shots <= 0)

    def reset(self):
        self.__D2.clear()
        self.__Q5.clear()
        self.__D2_droid = R2Droid(self.__rows, self.__cols, (2, 0), 5)
        self.__Q5_droid = R2Droid(self.__rows, self.__cols, (2, 3), 5)
        self.__D2_score = 0
        self.__Q5_score = 0
        self.__score_change = 0
        self.__time_remaining = 50
        self.__D2_label.config(text='D2\nScore: %d\nShots: %d\n%s' % (
            self.__D2_score, self.__D2_droid.shots, type(self.__D2).__name__))
        self.__Q5_label.config(text='Q5\nScore: %d\nShots: %d\n%s' % (
            self.__Q5_score, self.__Q5_droid.shots, type(self.__Q5).__name__))
        self.__time_label.config(
            text='Time Remaining: %d' % self.__time_remaining)
        self.__status_label.config(text='')
        self.__update_location()

    def run_episode(self, training=False):
        if self.__is_game_over():
            self.reset()
            return False
        self.__time_remaining = self.__time_remaining - 1
        next_D2_droid = self.__D2_droid.copy()
        next_Q5_droid = self.__Q5_droid.copy()
        D2_action = self.__D2.get_best_move(
            self.__D2_droid, self.__Q5_droid, self.__score_change, training)
        Q5_action = self.__Q5.get_best_move(
            self.__Q5_droid, self.__D2_droid, -self.__score_change, training)
        next_D2_droid.move_location(D2_action)
        next_Q5_droid.move_location(Q5_action)
        if next_D2_droid.location != next_Q5_droid.location and (
                self.__D2_droid.location != next_Q5_droid.location or
                self.__Q5_droid.location != next_D2_droid.location):
            self.__D2_droid = next_D2_droid
            self.__Q5_droid = next_Q5_droid
        self.__update_location()
        D2_score = int(self.__D2_droid.shoot(self.__Q5_droid, D2_action))
        Q5_score = int(self.__Q5_droid.shoot(self.__D2_droid, Q5_action))
        self.__display_laser(self.__D2_droid.location, D2_action, 'white')
        self.__display_laser(self.__Q5_droid.location, Q5_action, 'black')
        self.__score_change = D2_score - Q5_score
        if self.__score_change:
            self.__D2_score += D2_score
            self.__Q5_score += Q5_score
        self.__time_label.config(
            text='Time Remaining: %d' % self.__time_remaining)
        self.__D2_label.config(text='D2\nScore: %d\nShots: %d\n%s' % (
            self.__D2_score, self.__D2_droid.shots, type(self.__D2).__name__))
        self.__Q5_label.config(text='Q5\nScore: %d\nShots: %d\n%s' % (
            self.__Q5_score, self.__Q5_droid.shots, type(self.__Q5).__name__))
        if self.__is_game_over():
            text = 'Draw!'
            if self.__D2_score > self.__Q5_score:
                text = 'D2 Win!'
            elif self.__D2_score < self.__Q5_score:
                text = 'Q5 Win!'
            self.__status_label.config(text='Game Over! Result: ' + text)
        return True

    def train(self, episodes):
        if isinstance(self.__Q5, MinimaxAgent) and not isinstance(self.__D2, QAgent):
            print('Warning!!! No need to train MinimaxAgent!')
            return
        print('Training...')
        counter = 0
        last_percent = -1
        while counter < episodes:
            if self.run_episode(True):
                percent = counter * 100 // episodes
                if percent != last_percent and percent % 10 == 0:
                    print('%d%%' % percent, end='... ', flush=True)
                last_percent = percent
                counter += 1
        print('100%')


def run_gui():
    args = sys.argv[1:]
    if len(args) < 2:
        print('python3 r2d2_hw3.py [R2 Agent] [Q5 Agent] [Train Episodes]')
        print(
            'python3 r2d2_hw3.py KeyboardAgent [Q5 Agent] ([Train Episodes] [R2 Agent for Train])')
        return

    r2_agent = getattr(sys.modules[__name__], args[0])
    q5_agent = getattr(sys.modules[__name__], args[1])
    assert(issubclass(r2_agent, Agent) and issubclass(q5_agent, Agent))
    train_episodes = int(args[2]) if len(args) > 2 else 0

    if r2_agent == KeyboardAgent:
        act_r2_agent = None
        if len(args) > 3:
            act_r2_agent = getattr(sys.modules[__name__], args[3])
            assert(act_r2_agent is QAgent or act_r2_agent is MinimaxAgent)
            gui = GUI(act_r2_agent, q5_agent)
            gui.train(train_episodes)
            gui._GUI__D2 = KeyboardAgent()
        else:
            gui = GUI(r2_agent, q5_agent)
    else:
        gui = GUI(r2_agent, q5_agent)
        if train_episodes > 0:
            gui.train(train_episodes)

    gui.reset()
    gui.mainloop()


if __name__ == '__main__':
    run_gui()
