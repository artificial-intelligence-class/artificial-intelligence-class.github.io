from queue import PriorityQueue
from collections import defaultdict
from math import sqrt
inf = float('inf')

def null_heuristic(u, v):
    return 0

def manhattan_distance_heuristic(u, v):
    return sum(abs(x1-x2) for x1,x2 in zip(u,v))

def euclidean_distance_heuristic(u, v):
    return sqrt(sum((x1-x2)**2 for x1,x2 in zip(u,v)))

# adapted from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def A_star(G, start, goal, heuristic=null_heuristic):

    closedSet = set()
    openSet = set([start])
    frontier = PriorityQueue()
    parent = {}

    gScore = defaultdict(lambda:inf)  # gScore[v] = cost(start, v)
    gScore[start] = 0

    fScore = defaultdict(lambda:inf)  # fScore[v] = cost(start, v) + heuristic(v, goal)
    fScore[start] = heuristic(start, goal)
    frontier.put((fScore[start], start))

    while openSet:
        _, u = frontier.get()
        if u == goal:
            return reconstruct_path(start, goal, parent)

        try:
            openSet.remove(u)
        except:
            pass
        closedSet.add(u)

        for v in G.neighbors(u):
            if v in closedSet:
                continue

            tentative_gScore = gScore[u] + G.dist_between(u, v)

            if v not in openSet:
                openSet.add(v)
            elif tentative_gScore >= gScore[v]:
                continue

            parent[v] = u
            gScore[v] = tentative_gScore
            fScore[v] = gScore[v] + heuristic(v, goal)
            frontier.put((fScore[v], v))

            if v == goal:
                return reconstruct_path(start, goal, parent)

def reconstruct_path(start, goal, parent):
    path = [goal]
    current = goal
    while current != start:
        current = parent[current]
        path.append(current)
    return path[::-1]

