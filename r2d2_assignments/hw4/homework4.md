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





Word2vec is a very cool word embedding method that was developed by [Thomas Mikolov et al](https://www.aclweb.org/anthology/N13-1090) in 2013, as part of Google’s NLP team. You can read about it here, in [Chapter 6 of this book](https://web.stanford.edu/~jurafsky/slp3/6.pdf). To summarize: one of the ways you could represent words that commonly occur around it. For example, words the may appear in a 2 word window around burger may include words like delicious, tasty, ate, king, etc., that would identify it with other closely related food items. Then, if we wanted to represent a word, we could count how many times a context word appears around it. However, if we suppose our vocabulary has size 10,000, then our vectors would be very sparse.
One of the ways around this is to first fix a random size to the array, initialize random values, and then push target words closer to their context words.
One of the noteworthy things about the method is that it can be used to solve word analogy problems like:
<p align="center">
man is to king as woman is to [blank]
 </p>
 The way that it they take the vectors representing *king*, *man* and *woman* and perform some vector arithmetic to produce a vector that is close to the expected answer:
  <p align="center">
 $king−man+woman \approx queen$. 
 </p>.


However, one of the issues with word2vec is that it is not very good at capturing semantic meanings, and focuses more on context. For example, although front and ahead have similar semantic meanings, the similarity between Forward and front is 0.230, while the similarity between forward and ahead is 0.477. Similarly, one of the issues that word2vec runs into is that antonyms which have very similar context map onto similar vectors: the similarity between south and north is 0.967.
One of the nice things about antonyms matching together though is that the word2vec vectors have a good idea what kind of thing you want them to do. For example, north and south are both cardinal directions, and kick and punch have a good similarity score. We will try to leverage this fact to match R2D2 commands to the category of commands they belong to.

#### Getting Started with Magnitude and Downloading data

In the first part of the assigment, you will play around with the [Magnitude](https://github.com/plasticityai/magnitude)  library.  You will use Magnitude to load a vector model trained using word2vec, and use it to manipulate and analyze the vectors. Please refer [here](https://github.com/plasticityai/magnitude#installation) for the installation guidelines. 
In order to proceed further, you need to use the Medium Google-word2vec embedding model trained on Google News by using file `GoogleNews-vectors-negative300.magnitude` on eniac in `/home1/c/cis530/hw4_2019/vectors/`. ***WARNING, THIS FILE IS VERY LARGE, ~5GB
. MAKE SURE YOU HAVE ENOUGH SPACE BEFORE DOWNLOADING***
Once the file is downloaded, refer to the [Using the Libary](https://github.com/plasticityai/magnitude#using-the-library) section and the [Querying](https://github.com/plasticityai/magnitude#querying) section to see how to import and use the methods found in the library.

#### Assignment Questions

1.	What is the dimensionality of these word embeddings? Provide an integer answer.
2.	What are the top-5 most similar words to couch (not including couch itself)?
3.	According to the word embeddings, which of these words is not like the others? ['dodge_charger', 'ford_taurus', 'honda', 'lamborghini', 'tesla']
4.	Solve the following analogy: american is to dollar as japanese is to x. (10 points)
