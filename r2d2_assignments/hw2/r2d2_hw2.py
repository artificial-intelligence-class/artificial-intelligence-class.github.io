###Include your imports###
import math
import queue
import random
import itertools
from queue import Queue
from collections import defaultdict
import os

class Graph:
    def __init__(self, V, E):
        '''
            self.vertics -- store the vertics of a graph
            self.edges   -- store the edges of a graph
        '''
        pass

    def neighbors(self, u):
        '''
            return the neighbors of a grid
        '''
        pass

    def dist_between(self, u, v):
        '''
            calculate the distance between two grid
        '''
        pass

def BFS(G, start, goal):
    '''
        find solution using BFS search
    '''
    pass

def DFS(G, start, goal):
    '''
        find solution using DFS search
    '''
    pass

def A_star(G, start, goal):
    '''
        find solution using A* search
    '''
    pass

def tsp(G, start, goals):
    '''
        return the shortest path that passes all the goals
    '''
    pass

def path2move(path):
    '''
        convert finded path to movements
    '''
    pass

def r2d2_action(movement, droid, speed, time):
    '''
        convert movemnts to the commands for R2D2
    '''
    pass



##########Helper functions, Do not change##########

###generate vertics and edges to define a graph###
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

###Generate Random Map
def generate_random(row, column):
    vertics = [(i, j) for i in range(row) for j in range(column)]
    edges = []
    for vertic in vertics:
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_vertic = (vertic[0] + move[0], vertic[1] + move[1])
            if next_vertic in vertics:
                edges.append((vertic, next_vertic))

    num_of_barriers = round(row * 2 *column/3)
    barriers = random.sample(edges, num_of_barriers)
    for barrier in barriers:
        if barrier in edges:
            edges.remove(barrier)
        if random.random() > 0.15:

            if (barrier[1], barrier[0]) in edges:
                edges.remove((barrier[1], barrier[0]))

    return vertics, edges


###display the graph###
def printmap(G):
	rows = G.vertics[-1][0] + 1
	cols = G.vertics[-1][1] + 1
	for i in range(2 * rows - 1):
		print_row = ''
		if i % 2 == 0:
			for j in range(cols):
				current_node = (int(i / 2), j)
				right_node = (int(i / 2), j + 1)
				pattern = '☐'
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


###display the solution###
def printpath(G, start, goal, path):
	rows = G.vertics[-1][0] + 1
	cols = G.vertics[-1][1] + 1
	for i in range(2 * rows - 1):
		print_row = ''
		if i % 2 == 0:
			for j in range(cols):
				current_node = (int(i / 2), j)
				right_node = (int(i / 2), j + 1)
				if current_node == goal:
					pattern = '☒'
				elif current_node in path:
					pattern = '☑'
				else:
					pattern = '☐'
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

###########For GUI, Do not change#############
def parse_scene(scene_file):
    if not os.path.exists(scene_file):
        raise FileNotFoundError
    width = None
    height = None
    contents = []
    with open(scene_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if width is None:
                width = len(line)
            else:
                if len(line) != width:
                    raise ValueError
            tmp = []
            for char in line:
                if char == '.':
                    tmp.append(False)
                elif char == 'X':
                    tmp.append(True)
                else:
                    raise ValueError
            contents.append(tmp)

    height = len(contents)
    barriers = []
    for r in range(height):
        for c in range(width):
            if contents[r][c] is True:
                barriers.append((r, c))
    return {
        'rows': height,
        'columns': width,
        'scene': contents,
        'barriers': barriers
        }


def load_scene(scene_file):
    data = parse_scene(scene_file=scene_file)
    rows = data['rows']
    columns = data['columns']
    if rows < 2 or columns < 2:
        raise ValueError('the minimum size of a scene is 2x2')
    scene = data['scene']
    barriers = data['barriers']
    vertics, edges = generate_map_new(row=rows, column=columns, barriers=barriers)
    g = Graph(V=vertics, E=edges)
    return {
        'rows': rows,
        'columns': columns,
        'scene': scene,
        'graph': g
        }

def find_path_new(graph, method, start, goals):
    if not isinstance(graph, Graph):
        raise TypeError
    if not isinstance(start, tuple):
        raise TypeError
    if not isinstance(goals, list):
        raise TypeError
    if not goals:
        raise ValueError

    for point in goals:
        if point not in graph.vertics:
            raise ValueError

    if start not in graph.vertics:
        raise ValueError

    if method == 'dfs':
        func = DFS
    elif method == 'bfs':
        func = BFS
    elif method == 'a_star':
        func = A_star
    elif method == 'tsp':
        func = tsp
        if goals is None:
            raise ValueError
    else:
        raise NotImplementedError

    if method in ['dfs', 'bfs', 'a_star']:
        goals = goals[0]
        result = func(graph, start, goals)
        path = [result[0]]
        node_visited = result[1]
        return len(goals), path, node_visited
    else:
        # result = func(graph, start, goals)
        path = list(func(graph, start, goals))
        return len(goals), path
