import argparse
import math
import random
import time
import tkinter as tk
from enum import IntEnum
from functools import lru_cache
from typing import *

import agents


class State:
    def __init__(self, **grid):
        self._n, self._m = grid['size']
        self._pacman = grid['pacman']
        self._ghost = grid['ghost']
        self._dots = grid['dots']
        self.__walls = grid['conv_walls']
        if 'ghost_dir' in grid:
            self._ghost_dir = grid['ghost_dir']
        else:
            self._ghost_dir = random.choice(list(self._possible(self._ghost)))

    def __eq__(self, other: 'State'):
        return self._pacman == other._pacman and \
               self._ghost == other._ghost and \
               self._ghost_dir == self._ghost_dir and \
               self._dots == other._dots

    def __hash__(self):
        return hash((self._pacman, self._ghost, self._ghost_dir, self._dots))

    @property
    def _won(self):
        return len(self._dots) <= 0

    @property
    def _lost(self):
        return self._pacman == self._ghost

    def __oob(self, x, y):
        return x < 0 or x >= self._n or y < 0 or y >= self._m or self.__walls[x][y]

    def _possible(self, loc):
        x, y = loc
        possible = set()
        if not self.__oob(x - 1, y):
            possible.add(Pacman.Action.Up)
        if not self.__oob(x + 1, y):
            possible.add(Pacman.Action.Down)
        if not self.__oob(x, y - 1):
            possible.add(Pacman.Action.Left)
        if not self.__oob(x, y + 1):
            possible.add(Pacman.Action.Right)
        return possible

    @staticmethod
    def _do_action(loc, action):
        x, y = loc
        if action == Pacman.Action.Up:
            return x - 1, y
        if action == Pacman.Action.Down:
            return x + 1, y
        if action == Pacman.Action.Left:
            return x, y - 1
        return x, y + 1

    def _move(self, action):
        if action not in self._get_actions():
            raise ValueError('not a valid action')
        target_x, target_y = State._do_action(self._pacman, action)

        if self.__oob(target_x, target_y):
            pacman = self._pacman
        else:
            pacman = (target_x, target_y)

        dots = set(self._dots)
        if pacman in dots:
            dots.remove(pacman)

        ghost_poss = self._possible(self._ghost)
        if self._ghost_dir in ghost_poss:
            # no turning back unless wall is hit
            ghost_poss.discard(0b10 ^ self._ghost_dir)

        def calc_dist(d):
            p = self._do_action(self._ghost, d)
            return math.hypot(p[0] - pacman[0], p[1] - pacman[1])

        ghost_dir = random.choices(sorted(list(ghost_poss), key=calc_dist),
                                   weights=list(range(len(ghost_poss), 0, -1)))[0]

        new_ghost = self._do_action(self._ghost, ghost_dir)
        if self._pacman == new_ghost and pacman == self._ghost:
            x1, y1 = self._pacman
            x2, y2 = self._ghost
            pacman = new_ghost = (x1 + x2) / 2, (y1 + y2) / 2

        return State(
            size=(self._n, self._m),
            pacman=pacman,
            ghost=new_ghost,
            dots=tuple(sorted(dots)),
            conv_walls=self.__walls,
            ghost_dir=ghost_dir,
        )

    @lru_cache(maxsize=None)
    def _get_actions(self):
        x, y = self._pacman
        if x < 0 or x >= self._n or y < 0 or y >= self._m:
            raise ValueError('not a valid state')
        if self._lost or self._won:  # terminal
            return set()
        poss = set()
        all_poss = self._possible(self._pacman)
        for i in all_poss:
            poss.add(i)
            rev = 0b10 ^ i
            if rev in all_poss:
                poss.add(rev)
        return poss


class Pacman:
    class Action(IntEnum):
        Up = 3
        Down = 1
        Left = 0
        Right = 2

    @staticmethod
    def get_actions(state: State) -> Set[Action]:
        return state._get_actions()


class GUI(tk.Tk):
    SQUARE_SIZE = 50
    ANIMATION_SPEED = 0.1

    def __init__(self, grid, agent, init_state: State):
        super().__init__()

        self.__state = self.__init_state = init_state
        self.__agent = agent
        self.__last_action = Pacman.Action.Right

        rows, cols = grid['size']
        width = GUI.SQUARE_SIZE * (cols + 2)
        height = GUI.SQUARE_SIZE * (rows + 2)
        self.__canvas = tk.Canvas(self, width=width + 1, height=height + 1,
                                  highlightthickness=0, bg='black')
        # border
        self.__canvas.create_line(
            GUI.SQUARE_SIZE * .7, GUI.SQUARE_SIZE * .7,
            GUI.SQUARE_SIZE * (cols + 1.3), GUI.SQUARE_SIZE * .7,
            GUI.SQUARE_SIZE * (cols + 1.3), GUI.SQUARE_SIZE * (rows + 1.3),
            GUI.SQUARE_SIZE * .7, GUI.SQUARE_SIZE * (rows + 1.3),
            GUI.SQUARE_SIZE * .7, GUI.SQUARE_SIZE * .7,
            fill='blue', width=GUI.SQUARE_SIZE * .2
        )
        self.__canvas.create_line(*((_ + 1.5) * GUI.SQUARE_SIZE for _ in grid['walls']),
                                  fill='blue', width=GUI.SQUARE_SIZE * .2)
        self.__canvas.pack()

        self.__reward = tk.Label(self)
        self.__update_score(0)
        self.__reward.pack(side=tk.BOTTOM)

        self.title('Pacman - CIS 521')

    def __iterate(self, learning=True):
        if self.__state._lost or self.__state._won:
            result = self.__state._won
            self.__state = self.__init_state
            return result

        if learning:
            self.__last_action = self.__agent.get_action(self.__state)
        else:
            self.__last_action = self.__agent.get_best_policy(self.__state)
        new_state = self.__state._move(self.__last_action)
        reward = (len(new_state._dots) - len(self.__state._dots)) * 10 - 1
        if new_state._lost:
            reward -= 500
        elif new_state._won:
            reward += 500
        if learning:
            self.__agent.update(self.__state, self.__last_action, new_state, reward)
        self.__state = new_state
        return reward

    def __update_board(self):
        self.__canvas.delete('state')
        for x, y in self.__state._dots:
            self.__canvas.create_rectangle(
                (y + 1.4) * GUI.SQUARE_SIZE, (x + 1.4) * GUI.SQUARE_SIZE,
                (y + 1.6) * GUI.SQUARE_SIZE, (x + 1.6) * GUI.SQUARE_SIZE,
                tags='state', fill='white')

        x, y = self.__state._pacman
        self.__canvas.create_oval(
            (y + 1) * GUI.SQUARE_SIZE, (x + 1) * GUI.SQUARE_SIZE,
            (y + 2) * GUI.SQUARE_SIZE, (x + 2) * GUI.SQUARE_SIZE,
            tags='state', fill='yellow')
        pts = ((y + 1, x + 1), (y + 1, x + 2), (y + 2, x + 2), (y + 2, x + 1))
        self.__canvas.create_polygon(
            pts[self.__last_action][0] * GUI.SQUARE_SIZE,
            pts[self.__last_action][1] * GUI.SQUARE_SIZE,
            (y + 1.5) * GUI.SQUARE_SIZE, (x + 1.5) * GUI.SQUARE_SIZE,
            pts[(self.__last_action + 1) % 4][0] * GUI.SQUARE_SIZE,
            pts[(self.__last_action + 1) % 4][1] * GUI.SQUARE_SIZE,
            tags='state')

        x, y = self.__state._ghost
        self.__canvas.create_polygon(
            (y + 1) * GUI.SQUARE_SIZE, (x + 1) * GUI.SQUARE_SIZE,
            (y + 1) * GUI.SQUARE_SIZE, (x + 2) * GUI.SQUARE_SIZE,
            (y + 1 + 1 / 6) * GUI.SQUARE_SIZE, (x + 1.7) * GUI.SQUARE_SIZE,
            (y + 1 + 2 / 6) * GUI.SQUARE_SIZE, (x + 2) * GUI.SQUARE_SIZE,
            (y + 1 + 3 / 6) * GUI.SQUARE_SIZE, (x + 1.7) * GUI.SQUARE_SIZE,
            (y + 1 + 4 / 6) * GUI.SQUARE_SIZE, (x + 2) * GUI.SQUARE_SIZE,
            (y + 1 + 5 / 6) * GUI.SQUARE_SIZE, (x + 1.7) * GUI.SQUARE_SIZE,
            (y + 2) * GUI.SQUARE_SIZE, (x + 2) * GUI.SQUARE_SIZE,
            (y + 2) * GUI.SQUARE_SIZE, (x + 1) * GUI.SQUARE_SIZE,
            tags='state', fill='red', smooth=True)

        self.__canvas.create_oval(
            (y + 1.1) * GUI.SQUARE_SIZE, (x + 1.1) * GUI.SQUARE_SIZE,
            (y + 1.4) * GUI.SQUARE_SIZE, (x + 1.4) * GUI.SQUARE_SIZE,
            tags='state', fill='white', outline='white')
        self.__canvas.create_oval(
            (y + 1.6) * GUI.SQUARE_SIZE, (x + 1.1) * GUI.SQUARE_SIZE,
            (y + 1.9) * GUI.SQUARE_SIZE, (x + 1.4) * GUI.SQUARE_SIZE,
            tags='state', fill='white', outline='white')
        offset = (
            (y + 1.1, x + 1.2, y + 1.2, x + 1.3),
            (y + 1.6, x + 1.2, y + 1.7, x + 1.3),
            (y + 1.2, x + 1.3, y + 1.3, x + 1.4),
            (y + 1.7, x + 1.3, y + 1.8, x + 1.4),
            (y + 1.3, x + 1.2, y + 1.4, x + 1.3),
            (y + 1.8, x + 1.2, y + 1.9, x + 1.3),
            (y + 1.2, x + 1.1, y + 1.3, x + 1.2),
            (y + 1.7, x + 1.1, y + 1.8, x + 1.2),
        )
        self.__canvas.create_oval(
            *(_ * GUI.SQUARE_SIZE for _ in offset[::2][self.__state._ghost_dir]),
            tags='state', fill='black')
        self.__canvas.create_oval(
            *(_ * GUI.SQUARE_SIZE for _ in offset[1::2][self.__state._ghost_dir]),
            tags='state', fill='black')

    def __update_score(self, score):
        self.__reward.configure(text=f'Score: {score}')

    def train(self, episodes):
        rewards = []
        while len(rewards) < episodes:
            total = 0
            while True:
                reward = self.__iterate()
                if isinstance(reward, bool):
                    break
                total += reward
                self.__update_score(total)
            rewards.append(total)
            if len(rewards) % 100 == 0:
                print(f'{len(rewards)}/{episodes} completed')
                print(f'\tAverage rewards over all episodes: {sum(rewards) / len(rewards)}')
                print(f'\tAverage rewards for last 100 episodes: {sum(rewards[-100:]) / 100}')

    def play(self):
        total = 0
        while True:
            self.__update_board()
            self.update()
            time.sleep(self.ANIMATION_SPEED)

            reward = self.__iterate(learning=False)
            if isinstance(reward, bool):
                if reward:
                    print(f'Pacman won! Episode reward {total}')
                else:
                    print(f'Pacman lost! Episode reward {total}')
                return
            total += reward
            self.__update_score(total)


def convert_walls(size, walls):
    conv = [[False for _ in range(size[1])] for _ in range(size[0])]
    for k in range(len(walls) // 2 - 1):
        a, b, c, d = walls[k * 2], walls[(k + 1) * 2], walls[k * 2 + 1], walls[(k + 1) * 2 + 1]
        x1, x2 = min(a, b), max(a, b)
        y1, y2 = min(c, d), max(c, d)
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                conv[j][i] = True
    return conv


def identity_extractor(state, action):
    return {(state, action): 1.}


def closest_food(start, state: State):
    queue = [start]
    dist = {start: 0}
    while queue:
        pos = queue.pop(0)
        dist_n = dist[pos]
        if pos in state._dots:
            return dist_n
        for act in state._possible(pos):
            neighbor = state._do_action(pos, act)
            if neighbor not in dist:
                dist[neighbor] = dist_n + 1
                queue.append(neighbor)
    return None


@lru_cache(maxsize=10)
def simple_extractor(state, action):
    features = {'bias': 1}

    next_loc = state._do_action(state._pacman, action)

    features['ghost-step-away'] = next_loc == state._ghost or any(
        next_loc == state._do_action(state._ghost, act) for act in state._possible(state._ghost))

    if not features['ghost-step-away'] and next_loc in state._dots:
        features['food'] = 1

    dist = closest_food(next_loc, state)
    if dist is not None:
        features['closest-food'] = dist / (state._n * state._m)

    for k in features:
        features[k] /= 10
    return features


PRESET_LAYOUTS = {
    'small': {
        'size': (5, 5),
        'pacman': (0, 3),
        'ghost': (4, 2),
        'dots': ((2, 2), (4, 4)),
        'walls': (1, 1, 3, 1, 3, 3, 1, 3)
    },
    'medium': {
        'size': (5, 6),
        'pacman': (0, 0),
        'ghost': (4, 5),
        'dots': ((1, 1), (1, 4), (3, 1), (3, 4)),
        'walls': (2, 1, 2, 3)
    }
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
    parser.add_argument('layout', metavar='LAYOUT_NAME', help='layout preset', nargs='?',
                        choices=PRESET_LAYOUTS.keys(), default='small')
    parser.add_argument('-a', '--agent', help='Q learning agent type',
                        choices=('q', 'approx'), default='q')
    parser.add_argument('-f', '--feature', help='feature extraction type',
                        choices=('identity', 'simple'), default='identity')
    parser.add_argument('-d', '--discount', help='discount factor gamma (γ)',
                        type=argtype, default=0.8)
    parser.add_argument('-r', '--learning-rate', help='learning reward for Q agent',
                        type=float, default=0.2)
    parser.add_argument('-e', '--epsilon', help='exploration probability for Q agent (ε)',
                        type=float, default=0.05)
    parser.add_argument('-t', '--train', help='number of episodes to train', type=int,
                        required=True)
    parser.add_argument('-p', '--play', help='number of episodes to play', type=int, required=True)
    args = parser.parse_args()
    grid = PRESET_LAYOUTS[args.layout]
    if args.agent == 'q':
        agent = agents.QLearningAgent(Pacman, args.discount, args.learning_rate, args.epsilon)
    else:
        extractor = globals()[args.feature + '_extractor']
        agent = agents.ApproximateQAgent(
            Pacman, args.discount, args.learning_rate, args.epsilon, extractor=extractor)

    init_state = State(**grid, conv_walls=convert_walls(grid['size'], grid['walls']))
    gui = GUI(grid, agent, init_state)
    print(f'Start training {args.train} episodes...')
    gui.train(args.train)
    print(f'Start playing {args.play} episodes...')
    for i in range(args.play):
        gui.play()
        time.sleep(0.5)
    gui.mainloop()


if __name__ == '__main__':
    main()
