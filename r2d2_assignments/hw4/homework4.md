---
layout: default
img: new_robot_2x.png
img_link: https://xkcd.com/149/
caption: Natural Language Commands
title: CIS 521 Robot Excercise 4 "Commanding Robots with Natural Language" (Extra Credit)
active_tab: homework
release_date: 2019-11-12
due_date: 2019-10-26 23:59:00EST
materials:
    - 
      name: skeleton file
      url: r2d2_hw4.py 
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

For this assignment, you will edit and submit the following files:
=============================================================

- part1.txt
- part2.txt
- r2d2_hw4.py

Robot Excercise 4: Commanding Robots with Natural Language [XXX points]
=============================================================

## Instructions

This assignment will focus on natural language processing (NLP).  NLP is a vibrant subfield of artificial intelligence.  One of the goals of NLP is to allow computers to understand commands spoken in human language.  This enables technologies like Amazon Alexa, Apple's Siri or Google's Assistant. 

Word2vec is a very cool word embedding method that was developed by [Thomas Mikolov et al](https://www.aclweb.org/anthology/N13-1090) in 2013, as part of Google’s NLP team. You can read about it here, in [Chapter 6 of this book](https://web.stanford.edu/~jurafsky/slp3/6.pdf). To summarize: the intuition behind distributional word embeddings like Word2vec is that words that appear in similar contexts have similar meanings. Words that may appear in a 2 word window around burger may include words like delicious, tasty, ate, king, etc., that would identify it with other closely related food items that are also delicious, tasty, and ate, for example. Then, if we wanted to represent a word, we could count how many times a context word appears around it. Say when crawling over the entirety of Wikipedia, we find that the word "delicious" appears 6 times in total around the word "burger", we may have a 6 in the index for "delicious" in the vector for "burger". Our vectors can get really nasty with a vocabulary of size 10,000, not to mention that they would be very sparse as well.
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

## 1. R2D2 Commands [10 points]

Take a look at the file `r2d2TrainingSentences.txt`. We have 6 categories of commands, `state`, `direction`, `light`, `animation`, `head`, and `grid`. After reading these commands, we would realllyyyyyyy appreciate it if you could come up with 10 example sentences (distinct from the ones in `r2d2TrainingSentences.txt`), in a mix and match of these categories. Then, put these sentences in `part1.txt` in the syntax of the commands found in `r2d2TrainingSentences.txt`, where we have a `[category]Sentences :: Example sentence.` in each line. Do not worry about the punctuation of the sentence.

## Getting Started with Magnitude and Downloading data

To get accustomed with word2vec, you will play around with the [Magnitude](https://github.com/plasticityai/magnitude)  library.  You will use Magnitude to load a vector model trained using word2vec, and use it to manipulate and analyze the vectors. Please refer [here](https://github.com/plasticityai/magnitude#installation) for the installation guidelines. 
In order to proceed further, you need to use the Medium Google-word2vec embedding model trained on Google News by using file `GoogleNews-vectors-negative300.magnitude` on eniac in `/home1/c/cis530/hw4_2019/vectors/`. ***WARNING, THIS FILE IS VERY LARGE, ~5GB
. MAKE SURE YOU HAVE ENOUGH SPACE BEFORE DOWNLOADING***
Once the file is downloaded, refer to the [Using the Libary](https://github.com/plasticityai/magnitude#using-the-library) section and the [Querying](https://github.com/plasticityai/magnitude#querying) section to see how to import and use the methods found in the library.

## 2. Assignment Questions [10 points]

1.	What is the dimensionality of these word embeddings? Provide an integer answer.
2.	What are the top-5 most similar words to `couch` (not including `couch` itself)?
3.	According to the word embeddings, which of these words is not like the others? `['dodge_charger', 'ford_taurus', 'honda', 'lamborghini', 'tesla']`
4.	Solve the following analogy: `american` is to `dollar` as `japanese` is to x.

We have provided a file called `part2.txt` for you to submit answers to the questions above.

## 3. Intent Detection [XXX points]

In this section, we will try to leverage the individual word embeddings provided by word2vec using the Magnitude library, to try to detect the intent of random commands issued to the R2D2. Thus, given a input command, we want to find the category: `state`, `direction`, `light`, `animation`, `head`, or `grid`, to which it belongs to. One of the ways to do this is to create sentence/phrase embeddings out of the word embeddings we have.

1. **[5 points]** Write a function `sentenceToWords(sentence)` that returns a list of the words in a sentence, given a string `sentence` as input. The words in the list should all be lower case. Note that some words commonly have punctuation marks inside them, such as “accident-prone”. Our function should treat hyphenated words as one word. However, when passing in sentences you can assume that hyphenated words will come in the form of “accident_prone”, where an underscore separates the word instead. There is also one more case where punctuation can be “inside” a word. Your function should work like so:

    ```python
    >>> sentenceToWords("Due to his limp, Jack is accident_prone.")
    ['due', 'to', 'his', 'limp', 'jack', 'is', 'accident_prone']
    >>> sentenceToWords("REALLY?!")
    ['really']
    ```

2. **[5 points]** To determine how close two R2D2 commands are, we will need a method of determining the similarity of the two different vectors. We will use the cosign similarity metric. Recall from linear algebra that the dot product between two vectors v and w is:

> dot-product($\vec{v}, \vec{w}) = \vec{v} \cdot \vec{w} = \sum_{i=1}^{N}{v_iw_i} = v_1w_1 +v_2w_2 +...+v_Nw_N$

> The vector length of a vector c is defined as:

> $\|\vec{v}\| = \sqrt{\sum_{i=1}^{N}{v_i^2}}$

> And from linear algebra:

> $\frac{\vec{v} \cdot \vec{w}}{\|\vec{v}\|\|\vec{w}\|} =  cos \Theta$

> Where here, $\Theta$ represents the angle between v and w.

   Implement a cosign similarity function `def cosignSimilarity(vector1, vector2)`, where given two numpy vectors of similar length (feel free to use the numpy library), you return the cosign of the angles between them. You can verify that this is the method that the Magnitude library uses as well, by querying two words from the Magnitude library and using your own function to find the similarity, and compare that to Magnitude’s .similarity() function.
   
    ```python
    >>> from pymagnitude import *
    >>> vectors = Magnitude(path + "GoogleNews-vectors-negative300.magnitude")
    ...
    ```
    
    ```python
    >>> cosignSimilarity(np.array([2, 0]), np.array([0, 1]))
    0.0
    >>> vectors.similarity("cat", "dog")
    0.76094574
    >>> cosignSimilarity(vectors.query("cat"), vectors.query("dog"))
    0.76094574
    ```

3. **[5 points]** Now, given a sentence, implement the function `calcSentenceEmbedding(sentence)` that takes a sentence and returns a vector embedding for that sentence. You can assume that all the words in the sentence have the same importance, so addition of individual word vectors is fine. Your function should use the minimum amount of arithmetic necessary to achieve a vector representation for the sentence, where meanings can be compared accurately using cosign similarity.

4. **[10 points]** We have provided a txt file of training sentences for the R2D2s in a file named r2d2TrainingSentences.txt, as well as a function, `loadTrainingSentences(file_path)`, which reads the file and returns a dictionary with keys `[category]Sentences` which map to a list of the sentences belonging to that category.

    Write a function `sentenceToEmbeddings(commandTypeToSentences)` that converts every sentence in the dictionary returned by `loadTrainingSentences(file_path)` to an embedding. You should return a tuple of two elements. The first element is an m by n numpy array, where m is the number of sentences and n is the length of the vector embedding, and row i of the array contains the embedding for sentence i. The second element is a dictionary mapping from the index of the sentence to a tuple where the first element is the original sentence, and the second element is category, such as “direction”,. The order of the indices does not matter, but the indices of the matrix and the dictionary should match. i.e., sentence j should have an embedding in the jth row of the matrix, and should have itself and its category mapped onto by key j in the dictionary. The category should not contain the word `Sentences`.
    
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

    Simply finding the closest sentence and outputting that category may not be enough for this function. We suggest trying out a k-nearest neighbors approach, and scoring the neighbors in some way to find which category is the best fit. You can write new helper functions to help out. Which kind of words appear in almost all sentences and so are not a good way to distinguish sentence meanings?
        
    ```python
    >>> getCategory("Turn your lights green.", "data/r2d2TrainingSentences.txt")
    'light'
    >>> getCategory("Drive forward for two feet.", "data/r2d2TrainingSentences.txt")
    'direction'
    >>> getCategory("Do not laugh at me.", "data/r2d2TrainingSentences.txt")
    'no'
    ```
    
    Your implementation for this function can be as free as you want. We will test your function on a test set of sentences. Our training set will be ` r2d2TrainingSentences.txt `, and our test set will be similar to the development set called `r2d2DevelopmentSentences.txt` which we have provided for testing your implementation locally (however, there will be differences, so try not to overfit!). Your accuracy will be compared to scores which we believe are relatively achievable. Anything greater than or equal to a 75% accuracy on the test set will receive a 100%, and anything lower than a 60% accuracy will receive no partial credit. To encourage friendly competition, we have also set up a leaderboard so that you can see how well you are doing against peers (30 points).
    
*For Extra Extra Credit*

Take a look at this [online service](https://github.com/hanxiao/bert-as-service) which uses BERT. [BERT](https://arxiv.org/pdf/1810.04805.pdf) is one of the latest breakthroughs in NLP, and has broken previous state-of-the-art records on a number of tasks. With BERT, even without fine-tuning, you should easily be able to break through a 0.90 accuracy on our r2d2 test set. If you use BERT in your intent detection function `getCategory(sentence, file_path)`, either with Hanxiao's online service or in some other manner, we will manually give you extra extra credit.

## 4. Slot filling [15 points]

Now that we have a good idea which categories our commands belong to, we have to find a way to convert these commands to actions. This can be done via slot-filling, where given a natural language command we try to fill out slots corresponding to important values in the command. For example, given the slots NAME, RESTAURANT, TIME and HAS_RESERVED, and a command to a chat-bot such as "John wants to go to Olive Garden", the chat-bot should fill out the slots with values: {NAME: John, RESTAURANT: Olive Garden, TIME: N/A, HAS_RESERVED: False}, and then it can decide to either execute the command or ask for more information given the slot-values.

1. **[15 points]** Using regex or word2vec vectors, populate the functions `def lightParser(command)` and `def directionParser(command):` to perform slot-filling for the predefined slots, given string input `command`. We will test these functions and give you full credit if you get above a 50% accuracy. These functions do not have to be perfect, but the better these functions are, the better your R2D2 will respond to your commands.

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

## GIVE YOUR R2D2 LIFE

Now that you are finished with the intent detection and slot filling sections, you can now use the code you have written to try to talk to your R2D2! Perform the R2D2 server setup instructions found in previous R2D2 homeworks, and move all your files over to your `sphero-project/src` directory. Then, just change the ID in line 14 of `robot_com.py` to the ID of your robot, and on the command line run `python3 robot_com.py`.

Have fun! Try not to be too mean to your robot :).

*For More Extra Extra Credit* Integrate the Google Voice IPO like so: ETC
