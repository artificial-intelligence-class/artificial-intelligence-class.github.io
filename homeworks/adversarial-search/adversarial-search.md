---
layout: default
img: go.png
img_link: https://xkcd.com/1263/
caption: Go
title: CIS 521 Homework 4 "Games and Adversarial Search"
active_tab: homework
release_date: 2021-09-27
due_date: 2021-10-05 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: homeworks/adversarial-search/adversarial_search.py 
    -
        name: Dominoes Game GUI 
        url: homeworks/adversarial-search/dominoes_game_gui.py
submission_link: https://www.gradescope.com/courses/305169
---

<!-- Check whether the assignment is ready to release -->
{% capture today %}{{'now' | date: '%s'}}{% endcapture %}
{% capture release_date %}{{page.release_date | date: '%s'}}{% endcapture %}
{% if release_date > today %} 
<div class="alert alert-danger">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}
<!-- End of check whether the assignment is up to date -->

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
<li><a href="{{site.baseurl}}/{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}


Homework 4: Games and Adversarial Search [45 points]
=============================================================

## Instructions

In this assignment, you will implement an adversarial search algorithm to play the game dominoes. 

A skeleton file [adversarial_search.py](adversarial_search.py) containing empty definitions for each question has been provided. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed.

You may import definitions from any standard Python library, and are encouraged to do so in case you find yourself reinventing the wheel. If you are unsure where to start, consider taking a look at the data structures and functions defined in the `collections`, `copy`, and `itertools` modules.

You will find that in addition to a problem specification, most programming questions also include one or two examples from the Python interpreter. In addition to performing your own testing, you are strongly encouraged to verify that your code gives the expected output for these examples before submitting.

It is highly recommended that you follow the Python style guidelines set forth in [PEP 8](http://legacy.python.org/dev/peps/pep-0008/), which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}). 
You may submit as many times as you would like before the deadline, but only the last submission will be saved. 


## 1. Dominoes Games [40 points]

In this section, you will develop an AI for a game in which two players take turns placing $1 \\times 2$ dominoes on a rectangular grid.  There are no labels on the dominoes; each one can be considered identical to the others.  One player must always place their dominoes vertically, and the other must always place their dominoes horizontally. The last player who successfully places a domino on the board wins.

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
    
    In the `DominoesGame` class, write a method `legal_moves(self, vertical)` which yields the legal moves available to the current player (vertical player if vertical = True, otherwise the horizontal player) as (row, column) tuples. The moves should be generated in row-major order - When looking at the board as a 2-d array, your method should be visualizable as iterating through the rows from top to bottom, and within rows from left to right), starting from the top-left corner of the board.
    
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
    
    In the `DominoesGame` class, write a method `game_over(self, vertical)` that returns whether the current player (the vertical player if vertical = True, otherwise the horizontal player) is unable to place any dominoes.
    
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
    
    In the `DominoesGame` class, write a method `copy(self)` that returns a new `DominoesGame` object initialized with a deep copy of the current board. Changes made to the original puzzle should not be reflected in the copy, and vice versa.  For more information about the different types of copy available in standard python, see [this guide](https://docs.python.org/3/library/copy.html).
    
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
    
3. **[40 points]** In the `DominoesGame` class, write a method `get_best_move(self, vertical, limit)` which returns a $3$-element tuple containing the best move for the current player as a (row, column) tuple, its associated value (defined below), and the number of leaf nodes visited during the search. Recall that if the `vertical` parameter is `True`, then the current player intends to place a domino on squares `(row, col)` and `(row + 1, col)`, and if the `vertical` parameter is `False`, then the current player intends to place a domino on squares `(row, col)` and `(row, col + 1)`. Moves should be explored row-major order, described in further detail above, to ensure consistency.
    
    Your search should be a faithful implementation of the alpha-beta search given in the "Optimal Decisions in Games" section of the course textbook, with the restriction that you should look no further than `limit` moves into the future. To find a board's value, you should compute the number of moves available to the current player, then subtract the number of moves available to the opponent.
    
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

## 3. Feedback [5 points]

1. **[1 point]** Approximately how many hours did you spend on this assignment?

2. **[2 point]** Which aspects of this assignment did you find most challenging? Were there any significant stumbling blocks?

3. **[2 point]**  Which aspects of this assignment did you like? Is there anything you would have changed?
