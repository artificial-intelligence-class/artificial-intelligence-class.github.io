---
layout: default
img: chess-puzzle.png
img_link: https://www.explainxkcd.com/wiki/index.php/1002:_Game_AIs
caption: Chess Puzzle
title: CIS 521 Homework 1 Part 2 "Uninformed Search"
active_tab: homework
release_date: 2019-06-05
due_date: 2019-06-08 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: homework1_part2.py 
    - 
        name: Lights Out GUI
        url: homework1_lights_out_gui.py 
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



Homework 1 Part 2: Uninformed Search [40 points]
=============================================================

## Instructions

In this part, you will explore a classic puzzles from the perspective of uninformed search.

A skeleton file [homework1_part2.py](homework1_part2.py) containing empty definitions for each question has been provided. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed.

You may import definitions from any standard Python library, and are encouraged to do so in cases where you find yourself reinventing the wheel. If you are unsure where to start, consider taking a look at the data structures and functions defined in the `collections`, `itertools`, `math`, and `random` modules.

You will find that in addition to a problem specification, most programming questions also include a pair of examples from the Python interpreter. These are meant to illustrate typical use cases, and should not be taken as comprehensive test suites.

You are strongly encouraged to follow the Python style guidelines set forth in [PEP 8](http://www.python.org/dev/peps/pep-0008/), which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}).

You may submit as many times as you would like before the deadline, but only the last submission will be saved. 


## Lights Out [40 points]

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

Once you have implemented the functions and methods described in this section, you can play with an interactive version of the Lights Out puzzle using the GUI provided in the file [homework1_lights_out_gui.py](homework1_lights_out_gui.py) by running the following command:

    python3 homework1_lights_out_gui.py rows cols

The arguments `rows` and `cols` are positive integers designating the size of the puzzle.

In the GUI, you can click on a light to perform a move at that location, and use the side menu to scramble or solve the puzzle. The GUI is merely a wrapper around your implementations of the relevant functions, and may therefore serve as a useful visual tool for debugging.
