---
layout: default
active_tab: homework
img: new_robot_2x.png
img_link: https://xkcd.com/149/
caption: Natural Language Commands
title: CIS 521 Robot Excercise 5 "Commanding Robots with Natural Language" (Extra Credit)
attribution: This homework assignment was developed for UPenn's Artificial Intelligence class (CIS 521) in Fall 2019 John Zhang, Calvin Zhenghua Chen, and Chris Callison-Burch with help from Yrvine Thelusma and redesigned by Chenyu Liu, Jiaqi Liu and Yue Yang.
release_date: 2020-12-10
due_date: 2019-12-24 23:59:00EST
submission_link: https://www.gradescope.com/courses/160263
materials:
    - 
      name: notebook
      url: r2d2_hw5.ipynb
    - 
      name: sample
      url: sample.p
    - 
      name: test sentences
      url: test_sentences.p
readings:
-
   title: Dialogue Systems and Chatbots 
   authors: Dan Jurafsky and James H. Martin
   venue: Speech and Language Processing (3rd edition draft)
   type: textbook
   url: https://web.stanford.edu/~jurafsky/slp3/26.pdf
-
   title: Vector Semantics and Embeddings 
   authors: Dan Jurafsky and James H. Martin
   venue: Speech and Language Processing (3rd edition draft)
   type: textbook
   url: https://web.stanford.edu/~jurafsky/slp3/6.pdf
-
   title: Linguistic Regularities in Continuous Space Word Representations
   authors: Tomas Mikolov, Wen-tau Yih, Geoffrey Zweig
   venue: NACL 2013
   type: conference
   url: https://www.aclweb.org/anthology/N13-1090/
-
   title: Magnitude&colon; A Fast, Efficient Universal Vector Embedding Utility Package
   authors: Ajay Patel, Alexander Sands, Chris Callison-Burch, Marianna Apidianaki
   venue: ACL 2018
   type: conference
   url: https://www.aclweb.org/anthology/D18-2021/
-
   title: Learning to Parse Natural Language Commands to a Robot Control System
   authors: Cynthia Matuszek and Evan Herbst and Luke S. Zettlemoyer and Dieter Fox
   venue: ISER 2012
   type: conference
   url: https://homes.cs.washington.edu/~lsz/papers/mhzf-iser12.pdf
   optional: true
-
   title: Developing Skills for Amazon Alexa
   authors: Amazon
   type: website
   venue: developer tutorial
   url: https://developer.amazon.com/en-US/alexa/alexa-skills-kit
   optional: true
-
   title: Getting Started with Rasa
   authors: Rasa
   type: website
   venue: developer tutorial
   url: https://rasa.com/docs/getting-started/
   optional: true
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

Robot Excercise 5: R2D2 Intent Detection [100 points]
=============================================================


## Preface
R2D2’s speech recognition system is damaged in a collision. Now R2D2 cannot understand what Luke says and thus cannot assist him during combat. Your task is to implement a new intent detection module to help R2D2 classify different natural language commands.
 
## Instructions

This assignment will focus on a specific area in natural language processing (NLP) called intent detection. An intent detection module that will take in a natural language command, and determine what type of command that a user wants the droid to do. These will include things like driving commands, light commands, changing the position of its head, making sounds, etc.)

For example, the following command belongs to the category 'driving'.
```
"Drive straight ahead for 2 seconds at half speed"
```

A skeleton notebook [r2d2_hw5.ipynb](r2d2_hw5.ipynb) containing empty definitions for each question has been provided. Please do not change any of that. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed. You could use the [Google Colab](https://colab.research.google.com/) to edit the notebook file and conduct the training using the free GPU from Google. 

You are strongly encouraged to follow the Python style guidelines set forth in PEP 8, which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}).

## Part 0. Natural Language Commands for R2D2 [15 points]

We're going to begin this assignment by brainstorming different commands that we might like to give to our robot.  We'll take several factors into account:
1. What actions can the robot perform?
2. What are different ways that we can describe those actions?

The type of actions that our R2D2s can perform are dictated by its Python API.  You can see a list of the commands in the API like this:

<div class="container-fluid">
<div class="row">
<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">

### Driving API

```python
enter_drive_mode(self)
roll(self, speed, angle, time)
turn(self, angle, **kwargs)
update_position_vector(self, speed, angle, time)
roll_time(self, speed, angle, time, **kwargs)
roll_continuous(self, speed, angle, **kwargs)
restart_continuous_roll(self)
stop_roll(self, **kwargs) 
```
</div>

<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">

### Driving sentences

```python
driving_sentences = [
"Go forward for 2 feet, then turn right.",
"North is at heading 50 degrees.",
"Go North.",
"Go East.",
"Go South-by-southeast",
"Run away!",
"Turn to heading 30 degrees.",
"Reset your heading to 0",
"Turn to face North.",
"Start rolling forward.",
"Increase your speed by 50%.",
"Turn to your right.",
"Stop.",
"Set speed to be 0.",
"Set speed to be 20%",
"Turn around", ]
```
</div>




<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Lights API

```python
set_back_LED_color(self, r, g, b)
set_front_LED_color(self, r, g, b)
set_holo_projector_intensity(self, intensity)
set_logic_display_intensity(self, intensity)
```
</div>


<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Light sentences

```python
light_sentences = [
"Change the intensity on the holoemitter to maximum.",
"Turn off the holoemitter.",
"Blink your logic display.",
"Change the back LED to green.",
"Turn your back light green.",
"Dim your lights holoemitter.",
"Turn off all your lights.",
"Lights out.",
"Set the RGB values on your lights to be 255,0,0.",
"Add 100 to the red value of your front LED.",
"Increase the blue value of your back LED by 50%.",
"Display the following colors for 2 seconds each: red, orange, yellow, green, blue, purple.",
"Change the color on both LEDs to be green.", ]
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Head API

```python
rotate_head(self, angle)
```
</div>


<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Head sentences

```python
head_sentences = [
"Turn your head to face forward.",
"Look behind you.", ]
```
</div>


<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Variables about the droid's state


```python
angle = 0
awake = False
back_LED_color = (0, 0, 0)
battery(self)
connected_to_droid = False
continuous_roll_timer = None
drive_mode = False
drive_mode_angle = None
drive_mode_shift = None
drive_mode_spreed = None
front_LED_color = (0, 0, 0)
holo_projector_intensity = 0
logic_display_intensity = 0
stance = 2
waddling = False
```
</div>


<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Questions about variables 

```python
state_sentences = [
"What color is your front light?",
"Tell me what color your front light is set to.",
"Is your logic display on?",
"What is your stance?"
"What is your orientation?",
"What direction are you facing?",
"Are you standing on 2 feet or 3?",
"What is your current heading?",
"How much battery do you have left?",
"What is your battery status?",
"Are you driving right now?",
"How fast are you going?",
"What is your current speed?",
"Is your back light red?",
"Are you awake?", ]
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Connection API

```python
connect_to_R2D2(self)
connect_to_R2Q5(self)
disconnect(self)
scan(self)
exit(self)
```
</div>


<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Connection sentences

```python
connection_sentences = [
"Connect D2-55A2 to the server",
"Are there any other droids nearby?",
"Disconnect.",
"Disconnect from the server.", ]
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Stance API

```python
set_stance(self, stance, **kwargs)
set_waddle(self, waddle)
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Stance sentences

```python
stance_sentences = [
"Set your stance to be biped.",
"Put down your third wheel.",
"Stand on your tiptoes.",]
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Animations and sounds API

```python
animate(self, i, wait=3)
play_sound(self, soundID, wait=4)
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Animation sentences

```python
animation_sentences = [
"Fall over",
"Scream",
"Make some noise",
"Laugh",
"Play an alarm",]
```
</div>



<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Navigation on a grid
The following grid navigation commands are from the [Droid navigation assignment](hw2/homework2.html), not the provided API.  We will support grid navigation commands too.

```python 
Graph(vertics, edges)
A_star(G, start, goal)
path2move(path)
```
</div>


<div class="col-lg-6 col-md-6 col-xs-12" markdown="1">
### Navigation on a grid

```python 
grid_sentences = [
"You are on a 4 by 5 grid.",
"Each square is 1 foot large.",
"You are at position (0,0).",
"Go to position (3,3).",
"There is an obstacle at position 2,1.",
"There is a chair at position 3,3",
"Go to the left of the chair.",
"It’s not possible to go from 2,2 to 2,3.", ]
```
</div>

</div>
</div>

For each of the 8 categories of commands please create 10 unique sentences on how you might tell the robot to execute one or more of the actions in that category. You can add add your sentence lists to the code by adding them as arrays called `my_driving_sentences`, `my_light_sentences`, `my_head_sentences`, `my_state_sentences`, `my_connection_sentences`, `my_stance_sentences`, `my_animation_sentences`, and `my_grid_sentences`.

One of the amazing thing about language is that there are many different ways of communicating the same intent.  For example, if we wanted to have our R2D2 start waddling, we could say 
```python 
"waddle",
"totter",
"todder",
"teater",
"wobble",
"start to waddle"
"start waddling",
"begin waddling",
"set your stance to waddle",
"try to stand on your tiptoes",
"move up and down on your toes",
"rock from side to side on your toes",
"imitate a duck's walk",
"walk like a duck"
```
Similarly, if we wanted it to stop, we could prefix the command above with a bunch of ways of saying stop:
```python 
"stop your waddle",
"end your waddle",
"don't waddle anymore",
"stop waddling",
"cease waddling",
"stop standing on your toes",
"stand still"
"stop acting like a duck",
"don't walk like a duck",
"stop teetering like that"
"put your feet flat on the ground"
```

The goal of this part of the assignment is to enumerate as many ways of saying a command as you can think of (minimum of 10 per command group).  We will use these to train an intent detection module.  



## Recommended readings

<table>
   {% for publication in page.readings %}
    <tr>
      <td>
  {% if publication.url %}
    <a href="{{ publication.url }}">{{ publication.title }}.</a>
        {% else %}
    {{ publication.title }}.
  {% endif %}
  {{ publication.authors }}.
  {{ publication.venue }}.
</td></tr>
  {% endfor %}
</table>
