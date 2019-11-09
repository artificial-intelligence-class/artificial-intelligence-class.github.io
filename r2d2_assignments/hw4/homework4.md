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

1. **[5 points]** Write a function `sentenceToWords(sentence)` that returns a list of the words in a sentence, given a string `sentence` as input. The words in the list should all be lower case. Note that some words commonly have punctuation marks inside them, such as “accident-prone”. Our function should treat hyphenated words as one word. However, when passing in sentences you can assume that hyphenated words will come in the form of “accident_prone”, where an underscore separates the word instead. There is also one more case where punctuation can be “inside” a word.

2. **[5 points]** To determine how close two R2D2 commands are, we will need a method of determining the similarity of the two different vectors. We will use the cosign similarity metric. Recall from linear algebra that the dot product between two vectors v and w is:

> dot-product($\vec{v}, \vec{w}) = \vec{v} \cdot \vec{w} = \sum_{i=1}^{N}{v_iw_i} = v_1w_1 +v_2w_2 +...+v_Nw_N$

> The vector length of a vector c is defined as:

> $\|\vec{v}\| = \sqrt{\sum_{i=1}^{N}{v_i^2}}$

> And from linear algebra:

> $\frac{\vec{v} \cdot \vec{w}}{\|\vec{v}\|\|\vec{w}\|} =  cos \Theta$

Where here, $\Theta$ represents the angle between v and w.

Implement a cosign similarity function `def cosignSimilarity(vector1, vector2) `, where given two numpy vectors of similar length (feel free to use the numpy library), you return the cosign of the angles between them. You can verify that this is the method that the Magnitude library uses as well, by querying two words from the Magnitude library and using your own function to find the similarity, and compare that to Magnitude’s .similarity() function.

3. **[5 points]** Now, given a sentence, implement the function `calcSentenceEmbedding(sentence)` that takes a sentence and returns a vector embedding for that sentence. You can assume that all the words in the sentence have the same importance, so addition of individual word vectors is fine. Your function should use the minimum amount of arithmetic necessary to achieve a vector representation for the sentence, where meanings can be compared accurately using cosign similarity.

