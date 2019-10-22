---
layout: default
img: Darth_Vader.png
img_link: https://www.pinterest.com/pin/341851427962125071/?nic=1
caption: Darth Vader Copyright&#58; Pinterest
title: CIS 521 Robot Excercise 3 "Flag Capture Game" (Extra Credit)
active_tab: homework
release_date: 2019-10-24
due_date: 2019-11-7 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: r2d2_hw3.py
    - 
        name: R2D2 FlagCapture GUI
        url: r2d2_flag_capture_gui.zip
submission_link: https://www.gradescope.com/courses/59562
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
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}

Robot Excercise 3: Flag Capture Game using a Minimax Algorithm [100 points]
=============================================================
## Preface
The First Galactic Empire dispatched Darth Vader and their evil robot R2Q5 to distroy the base of Rebel Alliance. Our brave R2D2s will battle with the dark robots and capture the flag of Rebellion. We must also prevent the R2Q5s to capture the empire flag before us.

May the force be with you, go ahead, R2D2s. 

## Instructions
In this assignment, you will combine your knowledge of informed search algorithms with the adversarial search game tree to teach the R2D2s how to play optimally in a capture the flag game.

In this game, there will be two teams of two robots each. One team will consist of two D2 robots, and the other team will consist of two Q5 robots. The goal of the game is to have one of the teams "win" by capturing the flag corresponding to their team first.

A skeleton file [r2d2_hw3.py](r2d2_hw3.py) containing empty definitions for each question has been provided. Some helper functions and functions required for GUI are also provided. Please do not change any of that. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed.

You are strongly encouraged to follow the Python style guidelines set forth in PEP 8, which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}).

## 1. Create the Game Board [9 points]

1. **[2 points]** Similar to the navigation game in the last extra credit exerecise, the game board in this assignment also takes in the vertices and edges to define a graph. Along with these two parameters, we also need to define the position of the robots and the flags. These location vertices will be passed to the constructor for our `FlagCaptureGraph` game.

	```python
	def __init__(self, V, E, robots_pos, flags_pos):
		'''
			self.vertics --  store the vertices of the graph
			self.edges   --  store the edges of the graph
			self.robots_pos -- store the positions of the robots in a dictionary, keys = robot name, value = vertex
			self.flags_pos    -- store the positions of the flags
		'''
		pass
	```

	Given the inputs as shown, you should match the following outputs (the printmap function is already defined in our skeleton file - ```➀```, ```➁``` represent for the R2D2s, ```❶```, ```❷``` represent for the R2Q5s, ```⚐```, ```⚑``` are the flags of D2's and Q5's ):

	```python
	>>> V, E = generate_map(4, 4, [])
	>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
	>>> flags_pos = {'flag_D2': (3, 2), 'flag_Q5': (0, 1)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)
	>>> printmap(graph)
	➀   ⚑   ☐   ☐   
	               
	➁   ☐   ☐   ☐   
	               
	☐   ☐   ☐   ❶   
	               
	☐   ☐   ⚐   ❷   
	```

2. **[5 points]** ```neighbors(u)``` should take in a vertex ```u``` and return the list of vertices reachable from u (you don’t need to include ```u``` in that list and the order of the neighbors does not matter). Try to avoid recomputing neighborhoods every time the function is called since for large graphs this can waste a lot of time. In this function, you don't have to consider the positions of robots and flags.

	```python	
	def neighbors(self, u):
		'''
			Return the neighbors of a vertex.
		'''
		pass
	```
	With the `FlagCaptureGraph` variable graph as defined above, you should have:

	```python
	>>> graph.neighbors((0, 0))
	[(0, 1), (1, 0)]
	>>> graph.neighbors((0, 1))
	>>> [(0, 2), (1, 1), (0, 0)]
	```

3. **[2 points]** ```dist_between(u, v)``` should take in two vertices ```u``` and ```v``` and return 1 if there is an edge between ```u``` and ```v```, otherwise it should return None.

	```python
	def dist_between(self, u, v):
		'''
			Return the distance between two vertices.
		'''
		pass
	```

	```python
	>>> graph.dist_between((0, 0), (0, 1))
	1.0
	>>> graph.dist_between((0, 0), (1, 1))
	None
	```

## 2. Defining the Game Rules [36 points]

In this step, we will define the basic rules of the game, such as how to update the game state, what the successors of a state are, how to judge whether the game is over, etc.

1. **[4 points]** Implement ```game_over(self)``` to reflect whether a game is over or not. The criteria for a game being over is if a robot from a team is on its flag.

	```python
	>>> V, E = generate_map(4, 4, [])
	>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
	>>> flags_pos = {'flag_D2': (3, 2), 'flag_Q5': (0, 1)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)

	>>> graph.game_over()
	False

	>>> robots_pos = {'D2_1': (3, 2), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)

	>>> graph.game_over()
	True
	```

2. **[4 points]** ```islegalmove``` returns a boolean indicating if a movement is legal. The move direction includes 'north', 'south', 'east', 'west'. The robot shoult move within the game board and could only move to the neighbors of current grid. If there is a robot occupied at the grid you try to move, this movement will not be not legal.

	```python
	def islegalmove(self, move_robot, move_direction):
	'''
       Return a boolean indicating if a movement is legal
	'''
		pass
	```
	Keep using the given graph and robots/flags positions, you could expect the outputs shown below:

	```python
	>>> V, E = generate_map(4, 4, [])
	>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
	>>> flags_pos = {'flag_D2': (3, 2), 'flag_Q5': (0, 1)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)
	
	>>> graph.islegalmove('D2_1', 'east')
	True
	>>> graph.islegalmove('D2_1', 'south')
	False
	```

3. **[8 points]** ```legalmoves(self, move_robot)``` returns a list of all legal moves of a robot. Note that, if a robot is trapped (no move direction available), you should return 'stay' as its legal move.

	```python
	>>> graph.legalmoves('D2_1')
	['east']

	>>> graph.legalmoves('D2_2')
	['south', 'east']

	>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (0, 1), 'Q5_2': (1, 1)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)
	>>> printmap(graph)
	➀   ❶   ☐   ☐   
	               
	➁   ❷   ☐   ☐   
	               
	☐   ☐   ☐   ☐   
	               
	☐   ☐   ⚐   ☐   
	>>> graph.legalmoves('D2_1')
	['stay']
	```

4. **[8 points]** Implement the function: ```perform_move(self, robot, direction)``` to execute the movement of the robot and update the game accordingly. This function takes in the name of the robot to move and its move direction. Make sure to update ```self.robot``` after execute a movement. 

	```python
	>>> V, E = generate_map(4, 4, [])
	>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
	>>> flags_pos = {'flag_D2': (3, 2), 'flag_Q5': (0, 1)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)
	>>> printmap(graph)
	➀   ⚑   ☐   ☐   
	               
	➁   ☐   ☐   ☐   
	               
	☐   ☐   ☐   ❶   
	               
	☐   ☐   ⚐   ❷     

	>>> graph.perform_move('D2_1', 'east')
	>>> printmap(graph)
	☐   ➀   ☐   ☐   
	               
	➁   ☐   ☐   ☐   
	               
	☐   ☐   ☐   ❶   
	               
	☐   ☐   ⚐   ❷ 
	>>> graph.robots_pos
	{'D2_1': (0, 1), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)} 
	```

5. **[2 points]** Implement ```copy(self)``` to return a new `FlagCaptureGraph` object that is identical to the current, making a deep copy of the current map in doing so. You do not need to deep copy the vertex, edge, or flag parameters as these will not change during a game.

	```python
	>>> new_graph = graph.copy()
	>>> print(new_graph.robots_pos == graph.robots_pos)
	True
	>>> new_graph.perform_move('D2_1', 'east')
	>>> print(new_graph.robots_pos == graph.robots_pos)
	False
	```

6. **[10 points]** Implement the function: ```successors(self, D2)``` to generate the successors of a game state. The parameter D2 indicates whether it is the D2 team's turn. During each turn for a team, the robot 1 will move first and then the robot 2, meaning that if the first robot leaves a position, that position is open for the robot's teammate on its move. This function should yield a tuple where the first element is the movements of the two robots (a dictionary with keys of the robots and their next positions), as well as a copy of the new game map after these moves are performed. For the `FlagCaptureGraph` graph defined previously, we expect the following outputs:

	```python
	>>> V, E = generate_map(4, 4, [])
	>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
	>>> flags_pos = {'flag_D2': (3, 2), 'flag_Q5': (0, 1)}
	>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)

	>>> for move, game in graph.successors(D2 = True):
	...     print(move)
	...     printmap(game)
	... 
	{'D2_1': 'east', 'D2_2': 'south'}
	☐   ➀   ☐   ☐   
	               
	☐   ☐   ☐   ☐   
	               
	➁   ☐   ☐   ❶   
	               
	☐   ☐   ⚐   ❷  
	{'D2_1': 'east', 'D2_2': 'north'}
	➁   ➀   ☐   ☐   
	               
	☐   ☐   ☐   ☐   
	               
	☐   ☐   ☐   ❶   
	               
	☐   ☐   ⚐   ❷  
	{'D2_1': 'east', 'D2_2': 'east'}
	☐   ➀   ☐   ☐   
	               
	☐   ➁   ☐   ☐   
	               
	☐   ☐   ☐   ❶   
	               
	☐   ☐   ⚐   ❷  
	``` 
	```python
	>>> for move, game in graph.successors(D2 = False):
	...     print(move)
	...     printmap(game)
	... 
	{'Q5_1': 'north', 'Q5_2': 'north'}
	➀   ⚑   ☐   ☐   
	               
	➁   ☐   ☐   ❶   
	               
	☐   ☐   ☐   ❷   
	               
	☐   ☐   ⚐   ☐   
	{'Q5_1': 'north', 'Q5_2': 'west'}
	➀   ⚑   ☐   ☐   
	               
	➁   ☐   ☐   ❶   
	               
	☐   ☐   ☐   ☐   
	               
	☐   ☐   ❷   ☐  
	{'Q5_1': 'west', 'Q5_2': 'north'}
	➀   ⚑   ☐   ☐   
	               
	➁   ☐   ☐   ☐   
	               
	☐   ☐   ❶   ❷   
	               
	☐   ☐   ⚐   ☐  
	{'Q5_1': 'west', 'Q5_2': 'west'}
	➀   ⚑   ☐   ☐   
	               
	➁   ☐   ☐   ☐   
	               
	☐   ☐   ❶   ☐   
	               
	☐   ☐   ❷   ☐ 
	``` 

## 3. Define Your Utility Evaluate Function [25 points]

This part is open-ended, you should come up with a method to evaluate the utilities of the game. The evaluate function will have great impact on the performance of your robot and we will use the official method to play a game with your algorithm as the autograder. We will give your robots some advantages in the test cases and if your algorithm could beat us in 20 rounds, you could get the points.

## 4. Implement Minimax Algorithm with Alpha-beta Pruning [30 points]

In this part, you will utilize your knowledge of alpha-beta minimax algorithm to help the R2D2s find out the optimal movements.

```python
def get_best_move(self, D2, limit):
	'''
		D2 - boolean representing if it is the D2 team's turn
		limit - upper bound on the number of turns
		
		Return the best move, its utility value, and the total number of leaves encountered as
		(best_move, best_value, total_leaves)
	'''
	pass
```

Here, you are free to use whatever implementation of the minimax algorithm you want. However, we require that in your ```get_best_move``` function, your return value must be of the type ```best_move, best_value, total_leaves```, where ```best_move``` is the a movement (dictionary, syntax equivalent to the first element of the successors function), ```best_value``` is some value corresponding to what ```evaluate``` returns (won't be testing on this value), and ```total_leaves``` is the total number of leaf elements encountered, where a leaf is a finished goal state or any state after performing limit amount of moves. 

The inputs to the ```get_best_move``` function are D2, a boolean representing if it is the D2 team's turn, and limit, an upper bound on the number of turns to take. Here is an example of what outputs should look like:

```python
>>> V, E = generate_map(4, 4, [])
>>> robots_pos = {'D2_1': (0, 0), 'D2_2': (1, 0), 'Q5_1': (2, 3), 'Q5_2': (3, 3)}
>>> flags_pos = {'flag_D2': (3, 2), 'flag_Q5': (0, 1)}
>>> graph = FlagCaptureGraph(V, E, robots_pos, flags_pos)
>>> graph.get_best_move(D2 = True, limit = 4)
({'D2_1': 'east', 'D2_2': 'east'}, -3, 53)

>>> graph.get_best_move(D2 = False, limit = 4)
({'Q5_1': 'north', 'Q5_2': 'west'}, -3, 53)
```
Your results may be different because of your own method of evaluating the utilities. We won't grade on the results of your ```get_best_move```function. We will use the official method to play a game with your algorithm as the autograder. Your robots will be given some advantages in the test cases and if your algorithm could beat us in 20 rounds, you could get the points.

After you finished the minimax algorithm, you could now play the game in a virtual environment.

##5. Test Your Algorithm via the GUI

We provided a GUI for you to test your algorithm, [here](https://www.youtube.com/watch?v=WOnuUSAIqmQ) is a short video showing how to use the GUI. If you face any problems running the GUI, please post questions on piazza. The GUI has two interface shown as the figures below. The first one is for setting the system configurations. You could choose your scene or generate random scene given row and column number. You could also generate your own scene using the provided ```generate_scenes.py``` which will create a ```.sc``` file and will show up inside the pull-down menu of system configuration interface. The left side of game board interface shows the graph, the positions of the robots and flags. You need to follow the instructions on the right side to set the positions of the robots and flags at the begining. Then you could either press 1-9 to set the limit of your minimax algorithm to generate a best move for current robot or use arrow keys to play by yourself. By playing with your algorithm, you could find out whether your method to evaluate utilities is good or not.
![](GUI.png)

**[Find a partner]** You could also use the ```r2d2_flag_capture_gui_for_2_players.py``` to play the game with your friends to compare whose method is better. This GUI takes in two modules as imports and you could put your homework along with your friend's in the same folder and modify the file names just follow the instructions at the begining of the GUI file. Because we are also new to this project, there are still some bugs exist. If you face any problems using the GUI, please post questions on piazza and feel free to come to the OH.

##6. Play a Real World Game

You will apply your algorithm in the real robots to visulize your program. Remember to put your ```r2d2_hw3``` in the src folder of sphero project. 

You could implement an API to send commands to the robots to perform the movements. First, you need to connect to all of your robots using the following code.  

```python
>>> from client import DroidClient
###replace with your own tags###
>>> robot_tag = {'D2_1': 'D2-FE32', 'D2_2': 'D2-3493', 'Q5_1': 'Q5-D26A', 'Q5_2': 'Q5-B348'}
>>> droid1 = DroidClient()
>>> droid2 = DroidClient()
>>> droid3 = DroidClient()
>>> droid4 = DroidClient()
>>> Droids = {'D2_1': droid1, 'D2_2': droid2, 'Q5_1': droid3, 'Q5_2': droid4}
>>> for key in robot_tag:
...     Droids[key].connect_to_droid(robot_tag[key])
```

Then, you are required to write a function for rolling commands. ```r2d2_action(Droids, move_robot, move_direction, speed, time)``` takes in the ```Droids``` which is a dictionary storing all the droid clients. ```move_robot``` is the name of the robot to move and ```move_direction``` which could be ```'north'```, ```'south'```, ```'west'```, ```'east'``` and ```'stay'```. The ```speed``` and ```time``` should be adjusted according to the actual grid size. Note that the initial directions of the robots are all ```'north'``` which is 0 degree.

When you finish all the tasks above, you could now let your robots play a real world game! Click [here](https://www.youtube.com/watch?v=RpySn8pJcXA) to watch a demo of how the game plays. Type the following commands in the terminal and you will see ```Enter a limit or choose the directions for the robots: ``` which is waiting for the inputs. You could either type a number or two directions as inputs.

```python
###adjust the speed and time according to the grid size###
>>> speed = 0.4
>>> time = 1.5
>>> import r2d2_hw3 as X
>>> V, E = X.generate_map(4, 4, [])
>>> robots_pos = {'D2_1': (1, 2), 'D2_2': (2, 2), 'Q5_1': (1, 1), 'Q5_2': (2, 1)}
>>> flags_pos = {'flag_D2': (1, 0), 'flag_Q5': (2, 3)}
>>> graph = X.FlagCaptureGraph(V, E, robots_pos, flags_pos)
>>> X.playgame(graph, Droids, D2 = True, speed, time)
D2 Turn
Enter a limit or choose the directions for the robots: 3
Q5 Turn
Enter a limit or choose the directions for the robots: north west
```
