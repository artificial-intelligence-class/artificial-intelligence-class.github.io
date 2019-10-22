import math
import queue
import copy
from collections import defaultdict

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
        pass

    def neighbors(self, u):
        '''
        Return the neighbors of a vertex.
        '''
        pass

    def dist_between(self, u, v):
        '''
        Return the distance between two vertices.
        '''
        pass
    
    ##############################################
    ##                  Part 2                  ##
    ##############################################
    def copy(self):
        '''
        Return a deep copy of the current FlagCaptureGraph object
        '''
        pass
    def game_over(self):
        '''
        Return a boolean indicating if the game is over.
        '''
        pass

    def islegalmove(self, move_robot, move_direction):
        '''
        Return a boolean indicating if a movement is legal
        '''
        pass

    def legalmoves(self, move_robot):
        '''
        Return a list of all legal moves of a robot
        '''
        pass

    
    def perform_move(self, move_robot, move_direction):
        '''
        Execute the movement of the robot and update the game accordingly, updating robots_pos, flags_pos.
        '''
        pass

    def successors(self, D2):
        '''
        Generate the successors of a game state. The parameter D2 indicates whether it is 
        the D2 team's turn. This function should yield a tuple where the first element is
        the movements of the two robots (a dictionary with keys of the robots and their
        move directions), as well as a copy of the new game object after these moves are performed.
        '''
        pass
    
    ##############################################
    ##                  Part 3                  ##
    ##############################################
    def evaluate(self, D2):
        '''
        Return a numeric value (float/int) representing the utility for the D2 or Q5 team.
        '''
        pass
    
    ##############################################
    ##                  Part 4                  ##
    ##############################################
    def get_best_move(self, D2, limit):
        '''
        D2 - boolean representing if it is the D2 team's turn
        limit - upper bound on the number of turns
        
        Return the best move, its utility value, and the total number of leaves encountered as
        (best_move, best_value, total_leaves)
        '''
        pass

    ##############################################
    ##                  Part 5                  ##
    ##############################################
def r2d2_action(Droids, move_robot, move_direction, speed, time):
    
    pass

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

            


        
