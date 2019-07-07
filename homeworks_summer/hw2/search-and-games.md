---
layout: default
img: chess-puzzle.png
img_link: https://www.explainxkcd.com/wiki/index.php/1002:_Game_AIs
caption: Chess Puzzle
title: CIS 521 Homework 2 "Search and Games"
active_tab: homework
release_date: 2019-07-08
due_date: 2019-07-16 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: search_and_games.py
    - 
        name: Lights Out GUI
        url: lights_out_gui.py 
    - 
        name: Grid Navigation GUI
        url: grid_navigation_gui.py
    -
        name: Dominoes Game GUI 
        url: dominoes_game_gui.py
    - 
        name: simple scene
        url: scene_simple.txt
    - 
        name: barrier scene
        url: scene_barrier.txt
    - 
        name: random 50x50 scene
        url: scene_random.txt

submission_link: https://www.gradescope.com/courses/52017
---

<!-- Check whether the assignment is up to date -->
{% capture this_year %}{{'now' | date: '%Y'}}{% endcapture %}
{% capture due_year %}{{page.due_date | date: '%Y'}}{% endcapture %}
{% if this_year != due_year %} 
<div class="alert alert-danger">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}
<!-- End of check whether the assignment is up to date -->


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



Homework 2: Search and Games [100 points]
=============================================================

## Instructions

In this assignment, you will explore three classic puzzles from the perspective of search and games.

A skeleton file [search_and_games.py](search_and_games.py) containing empty definitions for each question has been provided. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed.

You may import definitions from any standard Python library, and are encouraged to do so in cases where you find yourself reinventing the wheel. If you are unsure where to start, consider taking a look at the data structures and functions defined in the `collections`, `itertools`, `math`, and `random` modules.

You will find that in addition to a problem specification, most programming questions also include a pair of examples from the Python interpreter. These are meant to illustrate typical use cases, and should not be taken as comprehensive test suites.

You are strongly encouraged to follow the Python style guidelines set forth in [PEP 8](http://www.python.org/dev/peps/pep-0008/), which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}).

You may submit as many times as you would like before the deadline, but only the last submission will be saved. 


## 1. Lights Out [40 points]

The Lights Out puzzle consists of an $m \\times n$ grid of lights, each of which has two states: on and off. The goal of the puzzle is to turn all the lights off, with the caveat that whenever a light is toggled, its neighbors above, below, to the left, and to the right will be toggled as well. If a light along the edge of the board is toggled, then fewer than four other lights will be affected, as the missing neighbors will be ignored.

In this section, you will investigate the behavior of Lights Out puzzles of various sizes by implementing a `LightsOutPuzzle` class. Once you have completed the problems in this section, you can test your code in an interactive setting using the provided GUI. See the end of the section for more details.

1. **[2 points]** A natural representation for this puzzle is a two-dimensional list of Boolean values, where `True` corresponds to the on state and `False` corresponds to the off state. In the `LightsOutPuzzle` class, write an initialization method `__init__(self, board)` that stores an input board of this form for future use. Also write a method `get_board(self)` that returns this internal representation. You additionally may wish to store the dimensions of the board as separate internal variables, though this is not required.
    

    ```python
    >>> b = [[True, False], [False, True]]
    >>> p = LightsOutPuzzle(b)
    >>> p.get_board()
    [[True, False], [False, True]]
    ```

    ```python
    >>> b = [[True, True], [True, True]]
    >>> p = LightsOutPuzzle(b)
    >>> p.get_board()
    [[True, True], [True, True]]
    ```
        
    
2. **[3 points]** Write a top-level function `create_puzzle(rows, cols)` that returns a new `LightsOutPuzzle` of the specified dimensions with all lights initialized to the off state.
    
    ```python
    >>> p = create_puzzle(2, 2)
    >>> p.get_board()
    [[False, False], [False, False]]
    ```

    ```python
    >>> p = create_puzzle(2, 3)
    >>> p.get_board()
    [[False, False, False],
     [False, False, False]]
    ```
    
3. **[5 points]** In the `LightsOutPuzzle` class, write a method `perform_move(self, row, col)` that toggles the light located at the given row and column, as well as the appropriate neighbors.
    
    ```python
    >>> p = create_puzzle(3, 3)
    >>> p.perform_move(1, 1)
    >>> p.get_board()
    [[False, True, False],
     [True,  True, True ],
     [False, True, False]]
    ```

    ```python
    >>> p = create_puzzle(3, 3)
    >>> p.perform_move(0, 0)
    >>> p.get_board()
    [[True,  True,  False],
     [True,  False, False],
     [False, False, False]]
    ```

4. **[5 points]** In the `LightsOutPuzzle` class, write a method `scramble(self)` which scrambles the puzzle by calling `perform_move(self, row, col)` with probability $1/2$ on each location on the board. This guarantees that the resulting configuration will be solvable, which may not be true if lights are flipped individually. After importing the `random` module with the statement `import random`, the expression `random.random() < 0.5` generates the values `True` and `False` with equal probability.
    
5. **[2 points]** In the `LightsOutPuzzle` class, write a method `is_solved(self)` that returns whether all lights on the board are off.
    
    ```python
    >>> b = [[True, False], [False, True]]
    >>> p = LightsOutPuzzle(b)
    >>> p.is_solved()
    False
    ```

    ```python
    >>> b = [[False, False], [False, False]]
    >>> p = LightsOutPuzzle(b)
    >>> p.is_solved()
    True
    ```
    
6. **[3 points]** In the `LightsOutPuzzle` class, write a method `copy(self)` that returns a new `LightsOutPuzzle` object initialized with a deep copy of the current board. Changes made to the original puzzle should not be reflected in the copy, and vice versa.
    
    ```python
    >>> p = create_puzzle(3, 3)
    >>> p2 = p.copy()
    >>> p.get_board() == p2.get_board()
    True
    ```

    ```python
    >>> p = create_puzzle(3, 3)
    >>> p2 = p.copy()
    >>> p.perform_move(1, 1)
    >>> p.get_board() == p2.get_board()
    False
    ```
    
7. **[5 points]** In the `LightsOutPuzzle` class, write a method `successors(self)` that yields all successors of the puzzle as (move, new-puzzle) tuples, where moves themselves are (row, column) tuples. The second element of each successor should be a new `LightsOutPuzzle` object whose board is the result of applying the corresponding move to the current board. The successors may be generated in whichever order is most convenient.
    
    ```python
    >>> p = create_puzzle(2, 2)
    >>> for move, new_p in p.successors():
    ...     print(move, new_p.get_board())
    ...
    (0, 0) [[True, True], [True, False]]
    (0, 1) [[True, True], [False, True]]
    (1, 0) [[True, False], [True, True]]
    (1, 1) [[False, True], [True, True]]
    ```

    ```python
    >>> for i in range(2, 6):
    ...     p = create_puzzle(i, i + 1)
    ...     print(len(list(p.successors())))
    ...
    6
    12
    20
    30
    ```
    
8. **[15 points]** In the `LightsOutPuzzle` class, write a method `find_solution(self)` that returns an optimal solution to the current board as a list of moves, represented as (row, column) tuples. If more than one optimal solution exists, any of them may be returned. Your solver should be implemented using a breadth-first graph search, which means that puzzle states should not be added to the frontier if they have already been visited, or are currently in the frontier. If the current board is not solvable, the value `None` should be returned instead. You are highly encouraged to reuse the methods defined in the previous exercises while developing your solution.
    
    *Hint:* For efficient testing of duplicate states, consider using tuples representing the boards of the `LightsOutPuzzle` objects being explored rather than their internal list-based representations. You will then be able to use the built-in `set` data type to check for the presence or absence of a particular state in near-constant time.
    
    ```python
    >>> p = create_puzzle(2, 3)
    >>> for row in range(2):
    ...     for col in range(3):
    ...         p.perform_move(row, col)
    ...
    >>> p.find_solution()
    [(0, 0), (0, 2)]
    ```

    ```python
    >>> b = [[False, False, False],
    ...      [False, False, False]]
    >>> b[0][0] = True
    >>> p = LightsOutPuzzle(b)
    >>> p.find_solution() is None
    True
    ```

Once you have implemented the functions and methods described in this section, you can play with an interactive version of the Lights Out puzzle using the GUI provided in the file [lights_out_gui.py](lights_out_gui.py) by running the following command:

    python3 lights_out_gui.py rows cols

The arguments `rows` and `cols` are positive integers designating the size of the puzzle.

In the GUI, you can click on a light to perform a move at that location, and use the side menu to scramble or solve the puzzle. The GUI is merely a wrapper around your implementations of the relevant functions, and may therefore serve as a useful visual tool for debugging.

## 2. Grid Navigation [30 points]

In this section, you will investigate the problem of navigation on a two-dimensional grid with obstacles. The goal is to produce the shortest path between a provided pair of points, taking care to maneuver around the obstacles as needed. Path length is measured in Euclidean distance. Valid directions of movement include up, down, left, right, up-left, up-right, down-left, and down-right.

Your task is to write a function `find_path(start, goal, scene)` which returns the shortest path from the start point to the goal point that avoids traveling through the obstacles in the grid. For this problem, points will be represented as two-element tuples of the form (row, column), and scenes will be represented as two-dimensional lists of Boolean values, with `False` values corresponding empty spaces and `True` values corresponding to obstacles. Your output should be the list of points in the path, and should explicitly include both the start point and the goal point. Your implementation should consist of an $A^\*$ search using the straight-line Euclidean distance heuristic. If multiple optimal solutions exist, any of them may be returned. If no optimal solutions exist, or if the start point or goal point lies on an obstacle, you should return the sentinal value `None`.

```python
>>> scene = [[False, False, False],
...          [False, True , False],
...          [False, False, False]]
>>> find_path((0, 0), (2, 1), scene)
[(0, 0), (1, 0), (2, 1)]
```

```python
>>> scene = [[False, True, False],
...          [False, True, False],
...          [False, True, False]]
>>> print(find_path((0, 0), (0, 2), scene))
None
```

Once you have implemented your solution, you can visualize the paths it produces using the provided GUI by running the following command:

    python3 grid_navigation_gui.py scene_path

The argument `scene_path` is a path to a scene file storing the layout of the target grid and obstacles. We use the following format for textual scene representation: `"."` characters correspond to empty spaces, and `"X"` characters correspond to obstacles.

## 3. Dominoes Games [30 points]

In this section, you will develop an AI for a game in which two players take turns placing $1 \\times 2$ dominoes on a rectangular grid. One player must always place his dominoes vertically, and the other must always place his dominoes horizontally. The last player who successfully places a domino on the board wins.

As with the Tile Puzzle, an infrastructure that is compatible with the provided GUI has been suggested. However, only the search method will be tested, so you are free to choose a different approach if you find it more convenient to do so.

The representation used for this puzzle is a two-dimensional list of Boolean values, where `True` corresponds to a filled square and `False` corresponds to an empty square.

1. **[0 point]** In the `DominoesGame` class, write an initialization method `__init__(self, board)` that stores an input board of the form described above for future use. You additionally may wish to store the dimensions of the board as separate internal variables, though this is not required.
    
2. **[0 point]** *Suggested infrastructure.*
    
    In the `DominoesGame` class, write a method `get_board(self)` that returns the internal representation of the board stored during initialization.
    
    ```python
    >>> b = [[False, False], [False, False]]
    >>> g = DominoesGame(b)
    >>> g.get_board()
    [[False, False], [False, False]]
    ```
    
    ```python
    >>> b = [[True, False], [True, False]]
    >>> g = DominoesGame(b)
    >>> g.get_board()
    [[True, False], [True, False]]
    ```
    
    Write a top-level function `create_dominoes_game(rows, cols)` that returns a new `DominoesGame` of the specified dimensions with all squares initialized to the empty state.
    
    ```python
    >>> g = create_dominoes_game(2, 2)
    >>> g.get_board()
    [[False, False], [False, False]]
    ```
    
    ```python
    >>> g = create_dominoes_game(2, 3)
    >>> g.get_board()
    [[False, False, False],
     [False, False, False]]
    ```
    
    In the `DominoesGame` class, write a method `reset(self)` which resets all of the internal board's squares to the empty state.
    
    ```python
    >>> b = [[False, False], [False, False]]
    >>> g = DominoesGame(b)
    >>> g.get_board()
    [[False, False], [False, False]]
    >>> g.reset()
    >>> g.get_board()
    [[False, False], [False, False]]
    ```
    
    ```python
    >>> b = [[True, False], [True, False]]
    >>> g = DominoesGame(b)
    >>> g.get_board()
    [[True, False], [True, False]]
    >>> g.reset()
    >>> g.get_board()
    [[False, False], [False, False]]
    ```
    
    In the `DominoesGame` class, write a method `is_legal_move(self, row, col, vertical)` that returns a Boolean value indicating whether the given move can be played on the current board. A legal move must place a domino fully within bounds, and may not cover squares which have already been filled.
    
    If the `vertical` parameter is `True`, then the current player intends to place a domino on squares `(row, col)` and `(row + 1, col)`. If the `vertical` parameter is `False`, then the current player intends to place a domino on squares `(row, col)` and `(row, col + 1)`. This convention will be followed throughout the rest of the section.
    
    ```python
    >>> b = [[False, False], [False, False]]
    >>> g = DominoesGame(b)
    >>> g.is_legal_move(0, 0, True)
    True
    >>> g.is_legal_move(0, 0, False)
    True
    ```
    
    ```python
    >>> b = [[True, False], [True, False]]
    >>> g = DominoesGame(b)
    >>> g.is_legal_move(0, 0, False)
    False
    >>> g.is_legal_move(0, 1, True)
    True
    >>> g.is_legal_move(1, 1, True)
    False
    ```
    
    In the `DominoesGame` class, write a method `legal_moves(self, vertical)` which yields the legal moves available to the current player as (row, column) tuples. The moves should be generated in row-major order (i.e. iterating through the rows from top to bottom, and within rows from left to right), starting from the top-left corner of the board.
    
    ```python
    >>> g = create_dominoes_game(3, 3)
    >>> list(g.legal_moves(True))
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    >>> list(g.legal_moves(False))
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    ```
    
    ```python
    >>> b = [[True, False], [True, False]]
    >>> g = DominoesGame(b)
    >>> list(g.legal_moves(True))
    [(0, 1)]
    >>> list(g.legal_moves(False))
    []
    ```
    
    In the `DominoesGame` class, write a method `perform_move(self, row, col, vertical)` which fills the squares covered by a domino placed at the given location in the specified orientation.
    
    ```python
    >>> g = create_dominoes_game(3, 3)
    >>> g.perform_move(0, 1, True)
    >>> g.get_board()
    [[False, True,  False],
     [False, True,  False],
     [False, False, False]]
    ```
    
    ```python
    >>> g = create_dominoes_game(3, 3)
    >>> g.perform_move(1, 0, False)
    >>> g.get_board()
    [[False, False, False],
     [True,  True,  False],
     [False, False, False]]
    ```
    
    In the `DominoesGame` class, write a method `game_over(self, vertical)` that returns whether the current player is unable to place any dominoes.
    
    ```python
    >>> b = [[False, False], [False, False]]
    >>> g = DominoesGame(b)
    >>> g.game_over(True)
    False
    >>> g.game_over(False)
    False
    ```
    
    ```python
    >>> b = [[True, False], [True, False]]
    >>> g = DominoesGame(b)
    >>> g.game_over(True)
    False
    >>> g.game_over(False)
    True
    ```
    
    In the `DominoesGame` class, write a method `copy(self)` that returns a new `DominoesGame` object initialized with a deep copy of the current board. Changes made to the original puzzle should not be reflected in the copy, and vice versa.
    
    ```python
    >>> g = create_dominoes_game(4, 4)
    >>> g2 = g.copy()
    >>> g.get_board() == g2.get_board()
    True
    ```
    
    ```python
    >>> g = create_dominoes_game(4, 4)
    >>> g2 = g.copy()
    >>> g.perform_move(0, 0, True)
    >>> g.get_board() == g2.get_board()
    False
    ```
    
    In the `DominoesGame` class, write a method `successors(self, vertical)` that yields all successors of the puzzle for the current player as (move, new-game) tuples, where moves themselves are (row, column) tuples. The second element of each successor should be a new `DominoesGame` object whose board is the result of applying the corresponding move to the current board. The successors should be generated in the same order in which moves are produced by the `legal_moves(self, vertical)` method.
    
    ```python
    >>> b = [[False, False], [False, False]]
    >>> g = DominoesGame(b)
    >>> for m, new_g in g.successors(True):
    ...     print(m, new_g.get_board())
    ...
    (0, 0) [[True, False], [True, False]]
    (0, 1) [[False, True], [False, True]]
    ```
    
    ```python
    >>> b = [[True, False], [True, False]]
    >>> g = DominoesGame(b)
    >>> for m, new_g in g.successors(True):
    ...     print(m, new_g.get_board())
    ...
    (0, 1) [[True, True], [True, True]]
    ```
    
    *Optional.*
    
    In the `DominoesGame` class, write a method `get_random_move(self, vertical)` which returns a random legal move for the current player as a (row, column) tuple. *The `random` module contains a function `random.choice(seq)` which returns a random element from its input sequence.*
    
3. **[30 points]** In the `DominoesGame` class, write a method `get_best_move(self, vertical, limit)` which returns a $3$-element tuple containing the best move for the current player as a (row, column) tuple, its associated value, and the number of leaf nodes visited during the search. Recall that if the `vertical` parameter is `True`, then the current player intends to place a domino on squares `(row, col)` and `(row + 1, col)`, and if the `vertical` parameter is `False`, then the current player intends to place a domino on squares `(row, col)` and `(row, col + 1)`. Moves should be explored row-major order, described in further detail above, to ensure consistency.
    
    Your search should be a faithful implementation of the alpha-beta search given on page 170 of the course textbook, with the restriction that you should look no further than `limit` moves into the future. To evaluate a board, you should compute the number of moves available to the current player, then subtract the number of moves available to the opponent.
    
    ```python
    >>> b = [[False] * 3 for i in range(3)]
    >>> g = DominoesGame(b)
    >>> g.get_best_move(True, 1)
    ((0, 1), 2, 6)
    >>> g.get_best_move(True, 2)
    ((0, 1), 3, 10)
    ```
    
    ```python
    >>> b = [[False] * 3 for i in range(3)]
    >>> g = DominoesGame(b)
    >>> g.perform_move(0, 1, True)
    >>> g.get_best_move(False, 1)
    ((2, 0), -3, 2)
    >>> g.get_best_move(False, 2)
    ((2, 0), -2, 5)
    ```
    

If you implemented the suggested infrastructure described in this section, you can play with an interactive version of the dominoes board game using the provided GUI by running the following command:

    python3 dominoes_game_gui.py rows cols

The arguments `rows` and `cols` are positive integers designating the size of the board.

In the GUI, you can click on a square to make a move, press 'r' to perform a random move, or press a number between $1$ and $9$ to perform the best move found according to an alpha-beta search with that limit. The GUI is merely a wrapper around your implementations of the relevant functions, and may therefore serve as a useful visual tool for debugging.
