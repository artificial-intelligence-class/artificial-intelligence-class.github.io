---
layout: default
img: new_pet.png
img_link: https://xkcd.com/413/
caption: import soul
title: CIS 521 Homework 2 "Robot Navigation with A\*"
active_tab: homework
release_date: 2018-08-10
due_date: 2018-09-11 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: homework2.py 
submission_link: https://www.gradescope.com/courses/52017
---

<!-- Check whether the assignment is up to date -->
<!--
{% capture this_year %}{{'now' | date: '%Y'}}{% endcapture %}
{% capture due_year %}{{page.due_date | date: '%Y'}}{% endcapture %}
{% if this_year != due_year %} 
<div class="alert alert-danger">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}


<div class="alert alert-info">
This assignment is due on {{ page.due_date | date: "%A, %B %-d, %Y" }} before {{ page.due_date | date: "%I:%M%p" }}. 
</div>

{% if page.materials %}
<div class="alert alert-info">
You can download the materials for this assignment here:
<ul>
{% for item in page.materials %}
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}


<div class="alert alert-info" markdown="span">
Links to tutorials and other Python resources are posted on the [schedule page](/lectures.html) in the Python Review parts.</div>


-->

Robot Excercise 2: Robot Navigation with A\* [0 points]
=============================================================

## Preface

During a reconnaissance mission gone wrong, R2D2 was attacked by Stormtroopers, leaving his executive control unit disconnected from his motor control unit. Luckily, R2D2's motor control unit can still access his 9G-capable network card. He just needs you to SSH into his motor control unit and guide him to the rendezvous with C3PO and Luke, but time is of the essence, so you must use A\* search to get him there as fast as possible. He just needs you to program and run the A\* search algorithm and integrate motor controls via his motor control unit API.

## Instructions

In this assignment, you'll learn the differences between "uninformed" search algorithms like BFS and DFS, and "informed" search algorithms like A\*. You will use both types of algorithms to solve multi-dimensional mazes and see how their performance compares (and save R2D2!).


## Part 1: Implement a Graph

In order to solve a maze, we first need to create a representation of a maze to run our algorithms on. We will implement our maze as a graph, where each vertex represents a grid cell, and an edge between vertices represents the ability to traverse between those grid cells.

There are many different ways we can implement a graph, and these design decisions will impact the running time of our algorithms. For this assignment, we will implement an *undirected*, *unweighted* graph with its edges stored as an *adjacency list*. 

Implement a graph with the following interface:

```
class Graph:

    def __init__(self, V, E):
        # TODO: implement

    def neighbors(self, u):
        # TODO: implement

    def dist_between(self, u, v):
        # TODO: implement
```

`Graph(V, E)` should take in a list of vertices `V = [v_1, v_2, ...]` and a list of edges `E = [(v_1, v_2), (v_3, v_4), ...]`. You should convert the list of edges into an adjacency list representation.

`neighbors(u)` should take in a vertex `u` and return the set of vertices reachable from `u` (you don't need to include `u` in that set). Try to avoid recomputing neighborhoods every time the function is called since for large graphs this can waste a lot of time.

`dist_between(u, v)` should take in two vertices `u` and `v` and return 1 if there is an edge between `u` and `v`, otherwise it should return `None`.


For example, for this 2x2 graph,

```
╭───╮   ╭───╮
│1,0╞═══╡1,1│
╰─╥─╯   ╰─╥─╯
  ║       ║
╭─╨─╮   ╭─╨─╮
│0,0│   │1,0│
╰───╯   ╰───╯
```

you could expect the following outputs:

```
>>> V = [(0, 0), (0, 1), (1, 0), (1, 1)]
>>> E = [((0,0), (0,1)), ((0,1), (1,1)), ((1,1), (1,0))]
>>> G = Graph(V, E)

>>> G.neighbors((0,0))
set([(1,0)])

>>> G.neighbors((0,1))
set([(0,0), (1,1)])

>>> G.dist_between((0,0), (0,1))
1

>>> G.dist_between((0,0), (1,0))
None
```

You might find the following cartesian product function useful when testing your graphs:

```
>>> from itertools import product
>>> list(product(range(3), range(3)))
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
```

## Step 2: Implement BFS and DFS

BFS and DFS, two algorithms that you will revisit again and again in this course, are two of the most primitive graph algorithms. Using pseudocode from [here](https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
) and [here](https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode) and the lecture slides, implement both of them from the skeleton code below:

```
from queue import Queue
from collections import defaultdict

def BFS(G, start, goal):
    frontier = Queue()
    discovered = defaultdict(lambda:False)
    parent = {}

    # TODO: implement
    
    return reconstruct_path(start, goal, parent)


def DFS_recursive(G, start, goal):
    discovered = defaultdict(lambda:False)
    parent = {}
    
    # TODO: implement

    return reconstruct_path(start, goal, parent)


def DFS_iterative(G, start, goal):
    discovered = defaultdict(lambda:False)
    parent = {}
    stack = []

    # TODO: implement

    return reconstruct_path(start, goal, parent)


def reconstruct_path(start, goal, parent):
    
    # TODO: implement

```

Since we know the goal vertex, the algorithms can stop once they have found a solution, however, note that this is not always the case when we are running these algorithms.

## Step 3: Implement A\* Search

Using the pseudocode [here](https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode) and the lecture slides, implement A\* search by filling in the TODOs:


```
from queue import PriorityQueue
from collections import defaultdict
from math import sqrt
inf = float('inf')

def A_star(G, start, goal, heuristic):

    closedSet = set()
    openSet = set([start])
    frontier = PriorityQueue()
    parent = {}

    gScore = defaultdict(lambda:inf)  # gScore[v] = cost(start, v)
    fScore = defaultdict(lambda:inf)  # fScore[v] = cost(start, v) + heuristic_cost(v, goal)

    # TODO: implement

    return reconstruct_path(start, goal, parent)


def reconstruct_path(start, goal, parent):
    
    # TODO: implement


def null_heuristic(u, v):
    # TODO: implement

def manhattan_distance_heuristic(u, v):
    # TODO: implement

def euclidean_distance_heuristic(u, v):
    # TODO: implement

```

Keep in mind that we would like the algorithm and heuristics to work for mazes of arbitrary dimensions.


## Step 4: Integrate R2D2's Motor Control API

R2D2 Motor Control Interface:
```
rotate(heading)
roll(heading, distance)
```

`rotate(heading)` rotates R2D2 `heading` degrees clockwise. For example, calling `rotate(90)` will turn R2D2 90° to the right, and calling `rotate(90)` again will turn R2D2 another 90° to the right (for a total of 180° relative to his original orientation). There is no functional difference between `rotate(-90)` and `rotate(270)`.

`roll(heading, distance)` rotates R2D2 `heading` degrees clockwise and then moves him forward `distance` units.

For example, the command sequence
```
roll(90, 1)
roll(180, 2)
roll(180, 1)
rotate(-90)
```
would result in R2D2 finishing in the same location with the same orientation that he started in.



```
def guide_r2d2(r2d2, path):
    # TODO: implement
```

Given a `path` and an `r2d2` object that implements the above interface, write a function that makes R2D2 follow the path. You can assume that a starting position of (0,0) represents the origin, the unit vector (1,0) represents movement along the +x-axis, and the unit vector (0,1) represents movement along the +y-axis. You can assume for this function that the path you are following is 2-dimensional.


## Step 5: Critical Thinking Questions

1.
    1. When might we use an informed search algorithm such as A\* rather than a shortest path algorithm (Bellman-Ford, Dijkstra)?
    2. Of the following algorithms, which are guaranteed to give a shortest path solution? Explain why or why not. (A counterexample is an acceptable argument.)
        1. BFS
        2. DFS
        3. A\*

2. In the context of A\* search:
    1. What is an admissable heuristic? Cite your source.
    2. What is the purpose of heuristics?

3. Run `python time_maze_solutions.py LENGTH WIDTH` with different maze sizes (e.g., 60x60, 150x150, 300x300) and look at the different statistics for each algorithm. You can see sample mazes by running `python generate_random_maze.py LENGTH HEIGHT`.
    1. Copy-paste the results you get for 100x100 mazes.
    2. Looking at your results:
        1. Which algorithm performed the best?
        2. Was it what you expected?
        3. Why do you think this algorithm performed the best?
        4. What changes in relative performance might you expect to see as the complexity of the problem (i.e., complexity and size of the problem and solution space) increases and why?
    3. Which A\* heuristic performed the best? Was it what you expected?
        1. How might the structures of the mazes affect the performance of the heuristics?
        2. What kind of maze structure would you expect the Manhattan distance heuristic to perform the worst on?
        3. What kind of maze structure would you expect the Manhattan distance heuristic to perform the best on?

