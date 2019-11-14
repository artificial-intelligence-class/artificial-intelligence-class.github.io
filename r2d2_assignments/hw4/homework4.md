---
layout: default
active_tab: homework
img: new_robot_2x.png
img_link: https://xkcd.com/149/
caption: Natural Language Commands
title: CIS 521 Robot Excercise 4 "Commanding Robots with Natural Language" (Extra Credit)
attribution: This homework assignment was developed for UPenn's Artificial Intelligence class (CIS 521) in Fall 2019 John Zhang, Calvin Zhenghua Chen, and Chris Callison-Burch with help from Yrvine Thelusma.
release_date: 2019-11-19
due_date: 2019-12-03 23:59:00EST
submission_link: https://www.gradescope.com/courses/59562
materials:
    - 
      name: skeleton file
      url: r2d2_hw4.py 
    - 
      name: part1.txt
      url: part1.txt
    - 
      name: part2.txt
      url: part2.txt
    - 
      name: audio_io.py
      url: audio_io.py
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

Robot Excercise 4: Commanding Robots with Natural Language [100 points]
=============================================================

## Instructions

This assignment will focus on natural language processing (NLP).  NLP is a vibrant subfield of artificial intelligence.  One of the goals of NLP is to allow computers to understand commands spoken in human language.  This enables technologies like Amazon Alexa, Apple’s Siri or Google’s Assistant.

Instead of issuing a command to your droid in Python like

```python
droid.roll(speed=0.5, heading=0, duration=2)
```

we are going to implement an NLP system that will allow you to say

```
"Drive straight ahead for 2 seconds at half speed"
```

Our NLP system will have three main components:

1. __An intent detection module__ that will take in a natural language command, and determine what type of command that a user wants the droid to do.  These will include things like direction commands, light commands, changing the position of its head, making sounds, etc.)
2. __A slot-filler module__ will take the command, and extract the arguments that need to be included when translating the natural language command into its Python equivalent. For example, light comands will need arguments like *which light* to set, and *what color* to change it to.
3. __A speech to text module__ that will allow you to speak into your computer’s microphone and have your voice command converted to text.  For this, we will use an API provided by Google.

<!--
## Background: Word Vectors

Word2vec is a very cool word embedding method that was developed by [Thomas Mikolov et al](https://www.aclweb.org/anthology/N13-1090) in 2013, as part of Google’s NLP team. You can read about it here, in [Chapter 6 of this book](https://web.stanford.edu/~jurafsky/slp3/6.pdf). To summarize: the intuition behind distributional word embeddings like Word2vec is that words that appear in similar contexts have similar meanings. Words that may appear in a 2 word window around burger may include words like delicious, tasty, ate, king, etc., that would identify it with other closely related food items that are also delicious, tasty, and ate, for example. Then, if we wanted to represent a word, we could count how many times a context word appears around it. Say, when crawling over the entirety of Wikipedia, we find that the word "delicious" appears 6 times in total around the word "burger". Then, maybe we could have a 6 in the index for "delicious" in the vector for "burger". Our vectors can get really nasty with a vocabulary of size 10,000, not to mention that they would be very sparse as well.

One of the ways around this is to first fix a size for the word vectors, initialize random values, and then push the vector representations of similar words together, using gradient descent to minimize some sort of distance function. More can be read about the methods the Word2vec strategy uses here: [Chapter 6 of this book](https://web.stanford.edu/~jurafsky/slp3/6.pdf). Word2vec provides small, fixed-dimensional vector embeddings of words, trained on a corpus of Google News articles which contained about 100 billion words.

One of the noteworthy things about the method is that it can be used to solve word analogy problems like:

<p align="center">
man is to king as woman is to [blank]
 </p>
 The way that it they take the vectors representing *king*, *man* and *woman* and perform some vector arithmetic to produce a vector that is close to the expected answer:
  <p align="center">
 $king−man+woman \approx queen$. 
 </p>.


Distributional word embeddings like Word2vec can run into the issue where antonyms, which have very similar contexts, map onto similar vectors: i.e., the similarity between "south" and "north" is 0.967.

One of the nice things about antonyms matching together though is that the word2vec vectors have a good idea what kind of thing you want them to do. For example, north and south are both cardinal directions, and kick and punch have a good similarity score. We will try to leverage this fact to match R2D2 commands to the category of commands they belong to.

## Getting Started with Magnitude and Downloading data

To get accustomed with word2vec, you will play around with the [Magnitude](https://github.com/plasticityai/magnitude)  library.  You will use Magnitude to load a vector model trained using word2vec, and use it to manipulate and analyze the vectors. Please refer [here](https://github.com/plasticityai/magnitude#installation) for the installation guidelines. 

In order to proceed further, you need to use the Medium Google-word2vec embedding model trained on Google News by using file `GoogleNews-vectors-negative300.magnitude` on eniac in `/home1/c/cis530/hw4_2019/vectors/`. *WARNING, THIS FILE IS VERY LARGE, ~5GB
. MAKE SURE YOU HAVE ENOUGH SPACE BEFORE DOWNLOADING*

Once the file is downloaded, refer to the [Using the Libary](https://github.com/plasticityai/magnitude#using-the-library) section and the [Querying](https://github.com/plasticityai/magnitude#querying) section to see how to import and use the methods found in the library.

## Questions about Magnitude [10 points]

1.  What is the dimensionality of these word embeddings? Provide an integer answer.
2.  What are the top-5 most similar words to `couch` (not including `couch` itself)?
3.  According to the word embeddings, which of these words is not like the others? `['dodge_charger', 'ford_taurus', 'honda', 'lamborghini', 'tesla']`
4.  Solve the following analogy: `american` is to `dollar` as `japanese` is to x.

We have provided a file called `part2.txt` for you to submit answers to the questions above.

-->

## 1. Natural Language Commands for R2D2 [10 points]

We're going to begin this assignment by brainstorming different commands that we might like to give to our robot.  We'll take several factors into account:
1. What actions can the robot perform?
2. What are different ways that we can describe those actions?

The type of actions that our R2D2s can perform are dictated by its Python API.  You can see a list of the commands in the API like this:

```python
from client import DroidClient
droid = DroidClient() 
droid.scan() 
droid.connect_to_droid('D2-55A2') # Replace D2-55A2 with your droid's ID
help(droid)
````

Let's put the API commands that help lists into different groups.  We'll also list natural langauge commands that might be associated with each group.  For the first part of this assignment, you will brainstrom 10 unique language commands for each group.  You will submit your sentences along with your code.

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

For each of the 8 categories of commands pleaese create 10 unique sentences on how you might tell the robot to execute one or more of the actions in that category. You can add add your sentence lists to the code by adding them as arrays called `my_driving_sentences`, `my_light_sentences`, `my_head_sentences`, `my_state_sentences`, `my_connection_sentences`, `my_stance_sentences`, `my_animation_sentences`, and `my_grid_sentences`.

One of the amazing thing about language is that there are many different ways of communicating the same intent.  For example, if we wanted to have our R2D2 start waddling, we could say 
```python 
"waddle",
"totter",
"todder",
"teater"
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



## 2. Intent Detection [65 points]

In this section, we will take in a new sentence that we have never seen before and try to classify what type of command the user wants to have the the robot execute.  To do so, we will measure the similarity of the user's new sentence with each of our training sentences.  We know what command group each of our training sentences belongs to, so we will find the nearest command sentences to the new sentence, and use their labels as the label of new sentence.  This is called $k$-nearest neighbor classification.   The label that we will assign will be `driving`, `light`, `head`, `state`, `connection`, `stance`, `animation`, or `grid`.

To calculate how similar two sentences are, we are going to leverage word embeddings that we dicussed in lecture (and that are described in the [Vector Semantics and Embeddings chapter of the Jurafsky and Martin textbook]).  We will use with pre-trained word2vec embeddings, and use the Magnitude python package work with the word embeddings.  We will create sentence embeddings out of the word embeddings for the words in the sentence.

<!--
1. **[5 points]** Write a function `sentenceToWords(sentence)` that returns a list of the words in a sentence, given a string `sentence` as input. The words in the list should all be **lower case**. Note that some words commonly have punctuation marks inside them, such as “accident-prone”. Our function should treat hyphenated words as **one** word. However, when passing in sentences you can assume that hyphenated words will come in the form of “accident_prone”, where an underscore separates the word instead. There is also one more case where punctuation can be “inside” a word. Your function should work like so:

    ```python
    >>> sentenceToWords("Due to his limp, Jack is accident_prone.")
    ['due', 'to', 'his', 'limp', 'jack', 'is', 'accident_prone']
    >>> sentenceToWords("REALLY?!")
    ['really']
    ```
-->
1. **[5 points]** Write a tokenization function `sentenceToWords(text)` which takes as input a string of text and returns a list of tokens derived from that text. Here, we define a token to be a contiguous sequence of non-whitespace characters.  We will remove punctuation marks and convert the text to lowercase. *Hint: Use the built-in constant `string.punctuation`, found in the `string` module.*
    
    ```python
    >>> tokenize("  This is an example.  ")
    ['this', 'is', 'an', 'example' ]
    ```
    
    ```python
    >>> tokenize("'Medium-rare,' she said.")
    ['medium', 'rare', 'she', 'said']
    ```

2. **[5 points]** Implement the cosine similarity fuction to compute how similar two  vectors. Here is the mathmatical definition of the different parts of the cosine function.  The __dot product__ between two vectors $$\vec{v}$$ and $$\vec{w}$$ is:
    
    $$\text{dot-product}(\vec{v}, \vec{w}) = \vec{v} \cdot \vec{w} = \sum_{i=1}^{N}{v_iw_i} = v_1w_1 +v_2w_2 +...+v_Nw_N$$
  
    The __vector length__ of a vector $$\vec{v}$$  is defined as:

    $$\|\vec{v}\| = \sqrt{\sum_{i=1}^{N}{v_i^2}}$$

    The __cosine__ of the angles between  $$\vec{v}$$  and $$\vec{w}$$ is:
    
    $$cos \Theta = \frac{\vec{v} \cdot \vec{w}}{\|\vec{v}\|\|\vec{w}\|}$$

    Here $$\Theta$$ represents the angle between $$\vec{v}$$ and $$\vec{w}$$.
    
    Implement a cosine similarity function `cosineSimilarity(vector1, vector2)`, where `vector1` and `vector2` are [numpy arrays](https://docs.scipy.org/doc/numpy/user/quickstart.html).  Your function should you return the cosine of the angles between them. You are welcome to use any of [the](https://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html#numpy.dot) [built-in](https://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html#numpy.sumsum) [numpy](https://docs.scipy.org/doc/numpy/reference/generated/numpy.square.html) [functions](https://docs.scipy.org/doc/numpy/reference/generated/numpy.sqrt.html)[.](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.norm.html) If you don't have numpy installed on your computer already, you should run `pip install numpy`.

    Here are some examples of what your method should output:

    ```python
    import numpy as np 
    ```

    ```python
    >>> cosineSimilarity(np.array([2, 0]), np.array([0, 1])) 
    0.0
    
    >>> cosineSimilarity(np.array([1, 1]), np.array([1, 1]))
    0.9999999999999998. # It's actually 1.0, but this is close enough.  

    >>> cosineSimilarity(np.array([10, 1]), np.array([1, 10]))
    0.19801980198019803

    >>> v1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> v2 = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    >>> cosineSimilarity(v1, v2)
    0.4210526315789473
    ```

<!--
    You can compare your implementation against the similarity method that the Magnitude library uses like this:
   
    ```python
    >>> from pymagnitude import *
    >>> vectors = Magnitude(path + "GoogleNews-vectors-negative300.magnitude")
    ...
    ```
    
    ```python
    >>> cosineSimilarity(np.array([2, 0]), np.array([0, 1])) # Your implementation
    0.0
    >>> vectors.similarity("cat", "dog") # Magnitude's implementation
    0.76094574
    >>> cosineSimilarity(vectors.query("cat"), vectors.query("dog")) # Your implementation
    0.76094574
   ```
--> 

3. **[5 points]** Next, we're going to compute the similarity of word vectors.  For this part, we'll use a pythong package Magnitude package. 

Now, given a sentence, implement the function `calcSentenceEmbedding(sentence)` that takes a sentence and returns a vector embedding for that sentence. 


You can assume that all the words in the sentence have the same importance, so addition of individual word vectors is fine. Your function should use the minimum amount of arithmetic necessary to achieve a vector representation for the sentence, where meanings can be compared accurately using cosine similarity.

4. **[10 points]** We have provided a txt file of training sentences for the R2D2s in a file named r2d2TrainingSentences.txt, as well as a function, `loadTrainingSentences(file_path)`, which reads the file and returns a dictionary with keys `[category]Sentences` which map to a list of the sentences belonging to that category.

    ```python
    >>> trainingSentences = loadTrainingSentences("data/r2d2TrainingSentences.txt")
    >>> trainingSentences['animationSentences']
    ['Fall over', 'Scream', 'Make some noise', 'Laugh', 'Play an alarm']
    ```

    Write a function `sentenceToEmbeddings(commandTypeToSentences)` that converts every sentence in the dictionary returned by `loadTrainingSentences(file_path)` to an embedding. You should return a tuple of two elements. The first element is an m by n numpy array, where m is the number of sentences and n is the length of the vector embedding. Row i of the array should contain the embedding for sentence i. The second element is a dictionary mapping from the index of the sentence to a tuple where the first element is the original sentence, and the second element is a category, such as “direction”. The order of the indices does not matter, but the indices of the matrix and the dictionary should match i.e., sentence j should have an embedding in the jth row of the matrix, and should have itself and its category mapped onto by key j in the dictionary. The category should not contain the substring `Sentences`.
    
    ```python
    >>> trainingSentences = loadTrainingSentences("data/r2d2TrainingSentences.txt")
    >>> sentenceEmbeddings, indexToSentence = sentenceToEmbeddings(trainingSentences)
    >>> sentenceEmbeddings[14:]
    array([[-0.05598213,  0.1943551 , -0.11834867, ..., -0.06152995,
             0.08182373, -0.09995176],
           [ 0.08825371,  0.11762686,  0.13814032, ..., -0.08913179,
            -0.01735716, -0.11799385],
           [ 0.0267941 ,  0.07393055,  0.16094553, ...,  0.01224081,
             0.30259034, -0.27123183],
           ...,
           [ 0.10430418, -0.1844649 ,  0.23166019, ...,  0.03172258,
             0.01876774,  0.08740467],
           [ 0.35799584,  0.15163158,  0.20712882, ..., -0.02359562,
             0.14265963, -0.31631052],
           [ 0.18705991, -0.02135478,  0.36185202, ..., -0.30548167,
             0.04913769, -0.20094341]])
    >>> indexToSentence[14]
    ('Turn to heading 30 degrees.', 'direction')
    ```

5. **[10 points]** Now, given an arbitrary input sentence, and an m by n matrix of sentence embeddings, write a function `closestSentence(sentence, sentenceEmbeddings)` that returns the index of the closest sentence to the input. This should be the row vector which is closest to the sentence vector of the input. Depending on the indices of your implementation of `sentenceToEmbeddings(commandTypeToSentences)`, the following output may vary.

    ```python
    >>> sentenceEmbeddings, _ = sentenceToEmbeddings(loadTrainingSentences("data/r2d2TrainingSentences.txt"))
    >>> closestSentence("Lights on.", sentenceEmbeddings)
    32
    ```

6. **[30 points]** Now, given an arbitrary input sentence, and a file path to r2d2 commands, write a function `getCategory(sentence, file_path)` that returns the category that that sentence should belong to. You should also map sentences that don’t really fit into any of the categories to a new category, “no”, and return “no” if the input sentence does not really fit into any of the categories.

    Simply finding the closest sentence and outputting that category may not be enough for this function. We suggest trying out a k-nearest neighbors approach, and scoring the neighbors in some way to find which category is the best fit. You can write new helper functions to help out. Also, which kind of words appear in almost all sentences and so are not a good way to distinguish between sentence meanings?
        
    ```python
    >>> getCategory("Turn your lights green.", "data/r2d2TrainingSentences.txt")
    'light'
    >>> getCategory("Drive forward for two feet.", "data/r2d2TrainingSentences.txt")
    'direction'
    >>> getCategory("Do not laugh at me.", "data/r2d2TrainingSentences.txt")
    'no'
    ```
    
    Your implementation for this function can be as free as you want. We will test your function on a test set of sentences. Our training set will be ` r2d2TrainingSentences.txt `, and our test set will be similar to the development set called `r2d2DevelopmentSentences.txt` which we have provided for testing your implementation locally (however, there will be differences, so try not to overfit!). Your accuracy will be compared to scores which we believe are relatively achievable. Anything greater than or equal to a 75% accuracy on the test set will receive a 100%, and anything lower than a 60% accuracy will receive no partial credit. To encourage friendly competition, we have also set up a leaderboard so that you can see how well you are doing against peers (30 points).

<!--
*For Extra Extra Credit*

Take a look at this [online service](https://github.com/hanxiao/bert-as-service) which uses BERT. [BERT](https://arxiv.org/pdf/1810.04805.pdf) is one of the latest breakthroughs in NLP, and has broken previous state-of-the-art records on a number of tasks. With BERT, even without fine-tuning, you should easily be able to achieve a 0.90 accuracy on our r2d2 test set. If you use BERT in your intent detection function `getCategory(sentence, file_path)`, either with Hanxiao's online service or in some other manner, we will manually give you extra extra credit.
-->


## 3. How good is your intent detection [5 points]

TODO - write an accuracy function, evaluate your intent detection module on a test set.


## 4. Slot filling [15 points]

Now that we have a good idea which categories our commands belong to, we have to find a way to convert these commands to actions. This can be done via slot-filling, which fills slots in the natural language command corresponding to important values. For example, given the slots NAME, RESTAURANT, TIME and HAS_RESERVED, and a command to a chat-bot such as "John wants to go to Olive Garden", the chat-bot should fill out the slots with values: {NAME: John, RESTAURANT: Olive Garden, TIME: N/A, HAS_RESERVED: False}, and then it can decide to either execute the command or ask for more information given the slot-values.

1. **[15 points]** Using regex or word2vec vectors, populate the functions `lightParser(command)` and `directionParser(command)` to perform slot-filling for the predefined slots, given string input `command`. We will test these functions and give you full credit if you get above a 50% accuracy. These functions do not have to be perfect, but the better these functions are, the better your R2D2 will respond to your commands.

    For `lightParser`, the `holoEmit` and `logDisp` indicate whether the command references the holoemitter or the logic display. If the command wants to add (increase), or subtract (decrease) RGB values, those slots should be true. The `on` and `off` fields correspond to whether the lights should be turned on or off, and should also respond to words like "maximum." The `lights` slot should be a list of which lights the command refers to, either `front` or `back`, or both if you believe your command refers to both lights.

    For `directionParser`, `increase` and `decrease` correspond to whether the command wants you to increase/decrease the speed, and `directions` correspond to a list of directions that appear in the command, in order. Directions should be one of `forward`, `back`, `left`, or `right`. Cardinal directions like "South" should map onto `back`, and "East" should map onto `right`, etc.

    Your functions should work like so:

    ```python
    >>> lightParser("Set your lights to maximum")
    {'holoEmit': False, 'logDisp': False, 'lights': ['front', 'back'], 'add': False, 'sub': False, 'off': False, 'on': True}
    >>> lightParser("Increase the red RGB value of your front light by 50.")
    {'holoEmit': False, 'logDisp': False, 'lights': ['front'], 'add': True, 'sub': False, 'off': False, 'on': False}
    ```
   
    ```python
    >>> directionParser("Increase your speed!")
    {'increase': True, 'decrease': False, 'directions': []}
    >>> directionParser("Go forward, left, right, and then East.")
    {'increase': False, 'decrease': False, 'directions': ['forward', 'left', 'right', 'right']}
    ```

## 5. Try it out!

Now that you are finished with the intent detection and slot filling sections, you can now use the code you have written to try to talk to your R2D2! Perform the R2D2 server setup instructions found in previous R2D2 homeworks, and move all your files over to your `sphero-project/src` directory. Then, just change the ID in line 14 of `robot_com.py` to the ID of your robot, and on the command line run `python3 robot_com.py`.

Try out commands like:

```python
"Change your lights to red, periwinkle, azure, green, and magenta."
```

Have fun! Try not to be too mean to your robot :).


## 6. Voice Input [Extra Extra Credit: 15 points]

*For More Extra Extra Credit* Integrate Google Cloud Platform speech-to-text module so that you can command your robot using voice!

Put robot_com.py and audio_io.py under the src folder. robot_com.py supports command line IO to control your robot using natural English language. With the addition of audio_io.py, you are able to control your robot using voice!

To run command line IO, you need to install matplotlib:

```
pip3 install matplotlib
```

You also need to uncomment code in robot_com.py, change the robot serial ID with your own, start the server in one Terminal, cd into the src folder in another Terminal and type:

```
python3 robot_com.py
```

To run audio IO, you will need to install portaudio and pyaudio:

```
brew install portaudio
pip3 install pyaudio
```

Next, you need to [sign up for a [Google Cloud Platform (GCP) account](https://cloud.google.com/gcp/). When you register a new account, you'll get $300 of free credits. You need to enable speech-to-text module, set up a new project and service account in your GCP account and get a service account key file (this is going to be in .json format). Rename it credentials.json and put it under the src folder. You may also need to install and set up Google Cloud SDK locally. Look up GCP's documentation for more details.

As before, change the robot serial ID with your own in audio_io.py. Make sure you recomment the code in robot_com.py if you decide to use voice IO.

To run voice IO, you need to start the server in one Terminal, cd into the src folder in another Terminal and type:

```
python3 audio_io.py
```

Notes:
1. If you want to try audio IO, please try command line IO first.

2. If you are able to successfully run audio_io.py, say your command (using voice!) and see if text appears in the Terminal. To end the session, simply say any sentence containing one of the following keywords: "exit", "quit", "bye" or "goodbye".





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
