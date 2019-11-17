import math
import queue
import copy
from collections import defaultdict
import random

class FlagCaptureGraph:
    
    ##############################################
    ##                  Part 1                  ##
    ##############################################
    def __init__(self, V, E, robots_pos, flags_pos):
        '''
        self.vertics --  store the vertices of the graph
        self.edges    --  store the edges of the graph
        self.robots_pos -- store the positions of the robots in a dictionary, keys = robot name, value = vertex
        self.flags_pos -- store the positions of the flags in a dictionary, keys = flag name, value = vertex
        '''
        self.vertics = V
        self.edges = E
        self.flags_pos = flags_pos
        self.robots_pos = robots_pos
        self.direct2vec = {'south': (1, 0), 'north': (-1, 0), 'east': (0, 1), 'west': (0, -1), 'stay': (0, 0)}
        self.adjacent = {}
        for node in self.vertics:
            neighbors = []
            for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                next_state = (node[0] + x, node[1] + y)
                if (node, next_state) in self.edges:
                    neighbors.append(next_state)
            self.adjacent[node] = neighbors
        self.cost = {}

    def neighbors(self, u):
        '''
        Return the neighbors of a vertex.
        '''
        return self.adjacent[u]

    def dist_between(self, u, v):
        '''
        Return the distance between two vertices.
        '''
        if v in self.neighbors(u):
            return math.sqrt(pow(u[0] - v[0], 2) + pow(u[1] - v[1], 2))
        else:
            return None
    
    ##############################################
    ##                  Part 2                  ##
    ##############################################
    def copy(self):
        '''
        Return a deep copy of the current FlagCaptureGraph object
        '''
        new_robots_pos = copy.deepcopy(self.robots_pos)
        new_flag_pos = copy.deepcopy(self.flags_pos)
        return FlagCaptureGraph(self.vertics, self.edges, new_robots_pos, new_flag_pos)

    def game_over(self):
        '''
        Return a boolean indicating if the game is over.
        '''
        if self.robots_pos['D2_1'] == self.flags_pos['flag_D2'] or self.robots_pos['D2_2'] == self.flags_pos['flag_D2'] or self.robots_pos['Q5_1'] == self.flags_pos['flag_Q5'] or self.robots_pos['Q5_2'] == self.flags_pos['flag_Q5']:
            return True
        else:
            return False

    def islegalmove(self, move_robot, move_direction):
        '''
        Return a boolean indicating if a movement is legal
        '''
        current_pos = self.robots_pos[move_robot]
        movement = self.direct2vec[move_direction]
        next_pos = (current_pos[0] + movement[0], current_pos[1] + movement[1])
        if next_pos in self.robots_pos.values():
            return False
        else:
            if (current_pos, next_pos) in self.edges:
                return True
            else:
                return False

    def legalmoves(self, move_robot):
        '''
        Return a list of all legal moves of a robot
        '''
        result = []
        for move_direction in ['south', 'north', 'east', 'west']:
            if self.islegalmove(move_robot, move_direction):
                result.append(move_direction)
        if len(result) == 0:
            result.append('stay')
        return result

    
    def perform_move(self, move_robot, move_direction):
        '''
        Execute the movement of the robot and update the game accordingly, updating robots_pos, flags_pos.
        '''
        if self.islegalmove(move_robot, move_direction) == False:
            return None
        movement = self.direct2vec[move_direction]
        current_pos = self.robots_pos[move_robot]
        self.robots_pos[move_robot] = (current_pos[0] + movement[0], current_pos[1] + movement[1])
    
    def successors(self, D2):
        '''
        Generate the successors of a game state. The parameter D2 indicates whether it is 
        the D2 team's turn. This function should yield a tuple where the first element is
        the movements of the two robots (a dictionary with keys of the robots and their
        move directions), as well as a copy of the new game object after these moves are performed.
        '''
        if D2 == True:
            for move_direction_1 in self.legalmoves('D2_1'):
                movement = {}
                movement['D2_1'] = move_direction_1
                new_game_1 = self.copy()
                new_game_1.perform_move('D2_1', move_direction_1)
                for move_direction_2 in new_game_1.legalmoves('D2_2'):
                    movement['D2_2'] = move_direction_2
                    new_game_2 = new_game_1.copy()
                    new_game_2.perform_move('D2_2', move_direction_2)
                    yield movement, new_game_2
        else:
            for move_direction_1 in self.legalmoves('Q5_1'):
                movement = {}
                movement['Q5_1'] = move_direction_1
                new_game_1 = self.copy()
                new_game_1.perform_move('Q5_1', move_direction_1)
                for move_direction_2 in new_game_1.legalmoves('Q5_2'):
                    movement['Q5_2'] = move_direction_2
                    new_game_2 = new_game_1.copy()
                    new_game_2.perform_move('Q5_2', move_direction_2)
                    yield movement, new_game_2

    
    
    ##############################################
    ##                  Part 3                  ##
    ##############################################
    def Astar(self, start, goal):
        if (start, goal) in self.cost:
            return self.cost[(start, goal)]
        else:
            node_visited = []
            q = queue.PriorityQueue()
            astar_cost_start = math.sqrt(pow(start[0] - goal[0],2) + pow(start[1] - goal[1],2))
            cost_start = 0
            path = [start]
            q.put((astar_cost_start, cost_start, path, start))
            
            while q.empty() != True:
                current_node = q.get()
                astar_cost, current_cost, path, current_pos = current_node[0], current_node[1], current_node[2], current_node[3]

                if current_pos == goal:
                    self.cost[(start, goal)] = (path, len(path))
                    return self.cost[(start, goal)]

                if current_pos not in node_visited:
                    node_visited.append(current_pos)
                    for node in self.neighbors(current_pos):
                        expand_cost = current_cost + math.sqrt(pow(node[0] - current_pos[0],2) + pow(node[1] - current_pos[1],2))
                        heuristic = math.sqrt(pow(node[0] - goal[0],2) + pow(node[1] - goal[1],2))
                        expand_astar_cost = expand_cost + heuristic
                        new_state = (expand_astar_cost, expand_cost, path + [node], node)
                        q.put(new_state)
            return self.cost[(start, goal)]

    def flagoccupy(self, D2):
        if D2 == True:
            if self.robots_pos['Q5_1'] == self.flags_pos['flag_D2'] or self.robots_pos['Q5_2'] == self.flags_pos['flag_D2']:
                return True
            else:
                return False
        else:
            if self.robots_pos['D2_1'] == self.flags_pos['flag_Q5'] or self.robots_pos['D2_2'] == self.flags_pos['flag_Q5']:
                return True
            else:
                return False

    def evaluate(self, D2):
        '''
        Return a numeric value (float/int) representing the utility for the D2 or Q5 team.
        '''
        cost_D2_1 = abs(self.robots_pos["D2_1"][0] - self.flags_pos["flag_D2"][0]) + abs(self.robots_pos["D2_1"][1] - self.flags_pos["flag_D2"][1])
        cost_D2_2 = abs(self.robots_pos["D2_2"][0] - self.flags_pos["flag_D2"][0]) + abs(self.robots_pos["D2_2"][1] - self.flags_pos["flag_D2"][1])
        cost_Q5_1 = abs(self.robots_pos["Q5_1"][0] - self.flags_pos["flag_Q5"][0]) + abs(self.robots_pos["Q5_1"][1] - self.flags_pos["flag_Q5"][1])
        cost_Q5_2 = abs(self.robots_pos["Q5_2"][0] - self.flags_pos["flag_Q5"][0]) + abs(self.robots_pos["Q5_2"][1] - self.flags_pos["flag_Q5"][1])

        if D2 == True:
            # if self.robots_pos['Q5_1'] == self.flags_pos['flag_D2'] or self.robots_pos['Q5_2'] == self.flags_pos['flag_D2']:
            #     return -100
            # elif self.robots_pos['D2_1'] == self.flags_pos['flag_Q5'] or self.robots_pos['D2_2'] == self.flags_pos['flag_Q5']:
            #     return 100
            return - min(cost_D2_1, cost_D2_2)
        else:
            # if self.robots_pos['Q5_1'] == self.flags_pos['flag_D2'] or self.robots_pos['Q5_2'] == self.flags_pos['flag_D2']:
            #     return 100
            # elif self.robots_pos['D2_1'] == self.flags_pos['flag_Q5'] or self.robots_pos['D2_2'] == self.flags_pos['flag_Q5']:
            #     return -100
            return - min(cost_Q5_1, cost_Q5_2)

    ##############################################
    ##                  Part 4                  ##
    ##############################################
    def alpha_beta_max(self, D2, original_D2, limit, alpha, beta):
        if limit <= 0 or self.game_over():
            return None, self.evaluate(original_D2), 1
        best_move, best_value, total_leaves = None, -float("inf"), 0
        for move, new_game in self.successors(D2):
            new_move, new_value, new_leaves = new_game.alpha_beta_min(
                not D2, original_D2, limit - 1, alpha, beta)
            total_leaves += new_leaves
            if new_value > best_value:
                best_move, best_value = move, new_value
            if best_value >= beta:
                break
            alpha = max(alpha, best_value)
        return best_move, best_value, total_leaves

    def alpha_beta_min(self, D2, original_D2, limit, alpha, beta):
        if limit <= 0 or self.game_over():
            return None, self.evaluate(original_D2), 1
        best_move, best_value, total_leaves = None, float("inf"), 0
        for move, new_game in self.successors(D2):
            new_move, new_value, new_leaves = new_game.alpha_beta_max(
                not D2, original_D2, limit - 1, alpha, beta)
            total_leaves += new_leaves
            if new_value < best_value:
                best_move, best_value = move, new_value
            if best_value <= alpha:
                break
            beta = min(beta, best_value)
        return best_move, best_value, total_leaves

    def get_best_move(self, D2, limit):
        '''
        D2 - boolean representing if it is the D2 team's turn
        limit - upper bound on the number of turns
        
        Return the best move, its utility value, and the total number of leaves encountered as
        (best_move, best_value, total_leaves)
        '''
        return self.alpha_beta_max(D2, D2, limit, -float("inf"),
            float("inf"))

    ##############################################
    ##                  Part 5                  ##
    ##############################################
def r2d2_action(Droids, move_robot, move_direction, speed, time):
    droid = Droids[move_robot]
    direct2deg = {'south': 180, 'north': 0, 'east': 90, 'west': 270}
    droid.roll(speed, direct2deg[move_direction], time)

####################################################
###########helper functions, do not change##########
####################################################

###Print the GameBoard###
def printmap(G):
    rows = G.vertics[-1][0] + 1
    cols = G.vertics[-1][1] + 1
    inv_robots_pos = {v: k for k, v in G.robots_pos.items()}
    inv_flags_pos = {v: k for k, v in G.flags_pos.items()}
    for i in range(2 * rows - 1):
        print_row = ''
        if i % 2 == 0:
            for j in range(cols):
                current_node = (int(i / 2), j)
                right_node = (int(i / 2), j + 1)
                pattern = '☐'
                if current_node in G.flags_pos.values():
                    if inv_flags_pos[current_node] == 'flag_D2':
                        pattern = '⚐'
                    elif inv_flags_pos[current_node] == 'flag_Q5':
                        pattern = '⚑'

                if current_node in G.robots_pos.values():
                    if inv_robots_pos[current_node] == 'D2_1':
                        pattern = '➀'
                    elif inv_robots_pos[current_node] == 'D2_2':
                        pattern = '➁'
                    elif inv_robots_pos[current_node] == 'Q5_1':
                        pattern = '❶'
                    elif inv_robots_pos[current_node] == 'Q5_2':
                        pattern = '❷'


                if (current_node, right_node) in G.edges and (right_node, current_node) in G.edges:
                    print_row += pattern + ' ' + '  '
                else:
                    if right_node in G.vertics:
                        print_row += pattern + ' ' + '| '
                    else:
                        print_row += pattern + ' ' + '  '
        else:
            for j in range(cols):
                current_node = (math.ceil(i/2), j)
                up_node = (math.ceil(i/2) - 1, j)
                if j == 0:
                    if (current_node, up_node) in G.edges and (up_node, current_node) in G.edges: 
                        print_row += '  ' + ' '
                    else:
                        print_row += '-- '
                else: 
                    if (current_node, up_node) in G.edges and (up_node, current_node) in G.edges:
                        print_row += '  ' + '  '
                    else:
                        print_row += '--- '
        print(print_row)

###Generate the map given barriers###
def generate_map(row, column, barriers):
    vertics = [(i, j) for i in range(row) for j in range(column)]
    edges = []
    for vertic in vertics:
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_vertic = (vertic[0] + move[0], vertic[1] + move[1])
            if next_vertic in vertics:
                edges.append((vertic, next_vertic))

    for barrier in barriers:
        edges.remove(barrier)
        edges.remove((barrier[1], barrier[0]))

    return vertics, edges

###generate a random map###
def generate_random(row, column):
    vertics = [(i, j) for i in range(row) for j in range(column)]
    edges = []
    for vertic in vertics:
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_vertic = (vertic[0] + move[0], vertic[1] + move[1])
            if next_vertic in vertics:
                edges.append((vertic, next_vertic))

    # num_of_barriers = random.randint(0, row * column)
    num_of_barriers = round(row * 2 *column/3)
    barriers = random.sample(edges, num_of_barriers)
    for barrier in barriers:
        if barrier in edges:
            edges.remove(barrier)
        if random.random() > 0.15:

            if (barrier[1], barrier[0]) in edges:
                edges.remove((barrier[1], barrier[0]))

    return vertics, edges

###Play real game###
def playgame(graph, Droids, D2, speed, time):
    valid_directions = ['north', 'east', 'west', 'south']
    if D2 == True:
        while graph.game_over() != True:
            print('*****D2 Turn*****')
            Input = input ("Enter a limit or choose the directions for the robots: ")
            if len(Input) == 1:
                limit = int(Input)
                D2_movements = graph.get_best_move(True, limit)[0]
                print(D2_movements)
                graph.perform_move('D2_1', D2_movements['D2_1'])
                graph.perform_move('D2_2', D2_movements['D2_2'])
                printmap(graph)
                r2d2_action(Droids, 'D2_1', D2_movements['D2_1'], speed, time)
                r2d2_action(Droids, 'D2_2', D2_movements['D2_2'], speed, time)
            else:
                Input = Input.split(' ')
                if len(Input) == 2:
                    D2_1_direction = Input[0]
                    D2_2_direction = Input[1]
                    if D2_1_direction in graph.legalmoves('D2_1'):
                        graph.perform_move('D2_1', D2_1_direction)
                        r2d2_action(Droids, 'D2_1', D2_1_direction, speed, time)
                    else:
                        print('Your input for D2_1 is not valid')

                    if D2_2_direction in graph.legalmoves('D2_2'):
                        graph.perform_move('D2_2', D2_2_direction)
                        r2d2_action(Droids, 'D2_2', D2_2_direction, speed, time)
                    else:
                        print('Your input for D2_2 is not valid')
                    printmap(graph)
                else:
                    print('Your input is not valid')
            if graph.game_over() == True:
                print('D2 WIN')
                break

            print('*****Q5 Turn*****')
            Input = input ("Enter a limit or choose the directions for the robots: ")
            if len(Input) == 1:
                limit = int(Input)
                Q5_movements = graph.get_best_move(False, limit)[0]
                print(Q5_movements)
                graph.perform_move('Q5_1', Q5_movements['Q5_1'])
                graph.perform_move('Q5_2', Q5_movements['Q5_2'])
                printmap(graph)
                r2d2_action(Droids, 'Q5_1', Q5_movements['Q5_1'], speed, time)
                r2d2_action(Droids, 'Q5_2', Q5_movements['Q5_2'], speed, time)
            else:
                Input = Input.split(' ')
                if len(Input) == 2:
                    Q5_1_direction = Input[0]
                    Q5_2_direction = Input[1]
                    if Q5_1_direction in graph.legalmoves('Q5_1'):
                        graph.perform_move('Q5_1', Q5_1_direction)
                        r2d2_action(Droids, 'Q5_1', Q5_1_direction, speed, time)
                    else:
                        print('Your input for Q5_1 is not valid')

                    if Q5_2_direction in graph.legalmoves('Q5_2'):
                        graph.perform_move('Q5_2', Q5_2_direction)
                        r2d2_action(Droids, 'Q5_2', Q5_2_direction, speed, time)
                    else:
                        print('Your input for Q5_2 is not valid')
                else:
                    print('Your input is not valid')
                printmap(graph)
            if graph.game_over() == True:
                print('Q5 WIN')
                break

    if D2 == False:
        while graph.game_over() != True:
            print('*****Q5 Turn*****')
            Input = input ("Enter a limit or choose the directions for the robots: ")
            if len(Input) == 1:
                limit = int(Input)
                Q5_movements = graph.get_best_move(False, limit)[0]
                print(Q5_movements)
                graph.perform_move('Q5_1', D2_movements['Q5_1'])
                graph.perform_move('Q5_2', D2_movements['Q5_2'])
                printmap(graph)
                r2d2_action(Droids, 'Q5_1', Q5_movements['Q5_1'], speed, time)
                r2d2_action(Droids, 'Q5_2', Q5_movements['Q5_2'], speed, time)
            else:
                Input = Input.split(' ')
                if len(Input) == 2:
                    Q5_1_direction = Input[0]
                    Q5_2_direction = Input[1]
                    if Q5_1_direction in graph.legalmoves('Q5_1'):
                        graph.perform_move('Q5_1', Q5_1_direction)
                        r2d2_action(Droids, 'Q5_1', Q5_1_direction, speed, time)
                    else:
                        print('Your input for Q5_1 is not valid')

                    if Q5_2_direction in graph.legalmoves('Q5_2'):
                        graph.perform_move('Q5_2', Q5_2_direction)
                        r2d2_action(Droids, 'Q5_2', Q5_2_direction, speed, time)
                    else:
                        print('Your input for Q5_2 is not valid')
                    printmap(graph)
                else:
                    print('Your input is not valid')
                printmap(graph)
            if graph.game_over() == True:
                print('Q5 WIN')
                break

            print('*****D2 Turn*****')
            Input = input ("Enter a limit or choose the directions for the robots: ")
            if len(Input) == 1:
                limit = int(Input)
                D2_movements = graph.get_best_move(True, limit)[0]
                print(D2_movements)
                graph.perform_move('D2_1', D2_movements['D2_1'])
                graph.perform_move('D2_2', D2_movements['D2_2'])
                printmap(graph)
                r2d2_action(Droids, 'D2_1', D2_movements['D2_1'], speed, time)
                r2d2_action(Droids, 'D2_2', D2_movements['D2_2'], speed, time)
            else:
                Input = Input.split(' ')
                if len(Input) == 2:
                    D2_1_direction = Input[0]
                    D2_2_direction = Input[1]
                    if D2_1_direction in graph.legalmoves('D2_1'):
                        graph.perform_move('D2_1', D2_1_direction)
                        r2d2_action(Droids, 'D2_1', D2_1_direction, speed, time)
                    else:
                        print('Your input for D2_1 is not valid')

                    if D2_2_direction in graph.legalmoves('D2_2'):
                        graph.perform_move('D2_2', D2_2_direction)
                        r2d2_action(Droids, 'D2_2', D2_2_direction, speed, time)
                    else:
                        print('Your input for D2_2 is not valid')
                    printmap(graph)
                else:
                    print('Your input is not valid')

                if graph.game_over() == True:
                    print('D2 WIN')
                    break

            


        
