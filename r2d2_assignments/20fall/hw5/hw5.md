---
layout: default
active_tab: homework
img: new_robot_2x.png
img_link: https://xkcd.com/149/
caption: Natural Language Commands
title: CIS 521 Robot Excercise 5 "Commanding Robots with Natural Language" (Extra Credit)
attribution: This homework assignment was developed for UPenn's Artificial Intelligence class (CIS 521) in Fall 2019 John Zhang, Calvin Zhenghua Chen, and Chris Callison-Burch with help from Yrvine Thelusma and redesigned by Chenyu Liu, Jiaqi Liu and Yue Yang.
release_date: 2021-11-23
due_date: 2021-12-15 23:59:00EST
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

Here are some sample commands: 

* **Driving:** "Go forward for 2 feet, then turn right.",
"North is at heading 50 degrees.",
"Go North.",
"Go East.",
"Go South-by-southeast",
"Run away!", "Turn to heading 30 degrees.",
"Reset your heading to 0",
"Turn to face North.",
"Start rolling forward."
* **Lights:** "Change the intensity on the holoemitter to maximum.",
"Turn off the holoemitter.",
"Blink your logic display.",
"Change the back LED to green.",
"Turn your back light green.",
"Dim your lights holoemitter.",
"Turn off all your lights.",
"Lights out."
* **Head:** "Turn your head to face forward.", "Look behind you."
* **State:** "What color is your front light?",
"Tell me what color your front light is set to.",
"Is your logic display on?",
"What is your stance?"
"What is your orientation?",
"What direction are you facing?",
"Are you standing on 2 feet or 3?"
* **Connection:** "Connect to the server",
"Are there any other droids nearby?",
"Disconnect.",
"Disconnect from the server."
* **Stance:** "Set your stance to be biped.",
"Put down your third wheel.",
"Stand on your tiptoes."
* **Animation:** "Fall over",
"Scream",
"Make some noise",
"Laugh",
"Play an alarm"
* **Grid:** "You are on a 4 by 5 grid.",
"Each square is 1 foot large.",
"You are at position (0,0).",
"Go to position (3,3).",
"There is an obstacle at position 2,1.",
"There is a chair at position 3,3",
"Go to the left of the chair.",
"It’s not possible to go from 2,2 to 2,3."


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

### Dataset
We collected thousands of students' written sentences from last year, and you could download the [sample](sample.p). The data is stored in the format of list of samples and each sample looks like this `[sentence, label]`. The label is the int range from 0 to 8 which denotes the category of this sentence. The map of label to category is shown below.

```python
ind2cat = {0: 'no', 1: 'driving', 2: 'light', 3: 'head', 4: 'state', 
		   5: 'connection', 6: 'stance', 7: 'animation', 8: 'grid'}
```

### Clean Text
Write a tokenization function clean(sentence) which takes as input a string of text and returns a list of tokens derived from that text. Here, we define a token to be a contiguous sequence of non-whitespace characters. We will remove punctuation marks and convert the text to lowercase, as well as remove the stopwords. Hint: Use the built-in constant string.punctuation, found in the string module, and/or python's regex library, re.

```python
>>> sentence = "Making beeping noises."
>>> clean(sentence)
['making', 'beeping', 'noises']
```
After you tokenize all sentences in training and validation set, you need to find the maximum number of tokens for all sentences and store it as `max_len`, this is a very important variable and we will use it multiple times later.

### Build a Vocabulary
Then we could use the tokenized data to construct a vocabulary. You need to first find the unique words in train/val set and count their occurrence number. Then we need to assign an index (start from 1) to each unique word.

```python
>>> word_count
{'making': 10,
 'beeping': 3,
 'noises': 7,...
>>> word2ind
{'making': 1,
 'beeping': 2,
 'noises': 3,...
```
Then we assign the size of the vocabulary to `vocab_size` which will be used for building the Recurrent Neural Network.

## Part 1: Recurrent Neural Network[10 points]
In this part, you will implement a RNN for intent detection. We will use [keras](https://keras.io) backbone in this section.

### Convert token to vector
Convert each list of tokens into an array use the vocabulary you built before. The length of the vector is the `max_len` and remember to do **zero\-padding** if tokens' lenghth is smaller than `max_len`. Please complete the `vectorize(tokens, max_len, word2ind)` function.

### One-hot label
Convert the scalar label to 1D array (length = 9), e.g `0 -> array([1, 0, 0, 0, 0, 0, 0, 0, 0])`

### Build the Recurrent Neural Network
Now it's time to build the RNN network to do the classification task, you could just refer to this [official document](https://www.tensorflow.org/guide/keras/rnn).

You will need the Embedding layer, RNN layer and Dense layer, your last layer should project to the number of labels. The architecture of model is shown below:

* Embedding Layer, Input Dimension = vocab_size, Output Dimension = 64
* Two LSTM layers with 64 Units
* Dense to the number of classes with softmax activation function

### Evaluate on test sentences
Now run your model to predict on the test sentences, you need to do the preprocessing on these sentences first and save your prediction to a list of labels, e.g `[0, 2, 1, 5, ....]`. Then save your prediction as `rnn.p` using the following code and submit to Gradescope.

```python
pickle.dump(test_prediction, open("rnn.p", "wb"))
```

## Part 2: Word Embedding[10 points]
In this part, instead of build the vocabulary and use word2index to vectorize the tokens, we are going to leverage word embeddings that we dicussed in lecture (and that are described in the [Vector Semantics and Embeddings chapter of the Jurafsky and Martin textbook](http://web.stanford.edu/~jurafsky/slp3/6.pdf)).  We will use pre-trained word2vec embeddings, and use the Magnitude python package to work with these embeddings. Then, we will use the embeddings for the words in a sentence to create sentence embeddings.

### pymagnitude
For this part, we'll use the [Magnitude package](https://github.com/plasticityai/magnitude), which is a fast, efficient Python package for manipulating pre-trained word embeddings.  It was written by former Penn students Ajay Patel and Alex Sands.  You can install it with pip by typing this command into your terminal:

```bash
pip3 install pymagnitude
```

Next, you'll need to download a pre-trained set of word embeddings.  We'll get a set trained with Google's word2vec algorithm, which we discussed in class.  You can download them by clicking on [this link](http://magnitude.plasticity.ai/word2vec/medium/GoogleNews-vectors-negative300.magnitude) or by using this command in your terminal:

```bash
wget http://magnitude.plasticity.ai/word2vec/medium/GoogleNews-vectors-negative300.magnitude
```
**Warning:** the file is very large (5GB).  If you'd like to experiment with another set of word vectors that is smaller, you can [download these GloVE embeddings](http://magnitude.plasticity.ai/glove/heavy/glove.6B.300d.magnitude) which are only 1.4GB.

[Here](https://gitlab.com/Plasticity/magnitude), you can check the full list of available embeddings, feel free to try different embeddings.

```python
from pymagnitude import *
vectors = Magnitude("GoogleNews-vectors-negative300.magnitude") 
v = vectors.query("cat") # vector representing the word 'cat'
w = vectors.query("dog") # vector representing the word 'dog'
```

### Convert tokens to embeddings
You could now use the pymagnitude to query each token and convert them to a list of embeddings. Note that you need to do zero padding to match the maximum length. Please complete the `embedding(list_tokens, max_len, vectors)`.

### Build the RNN model
Similar to Part 1, build a RNN model using your new embedding. The model architecture is shown below.

* LSTM Layer with input shape (max_len, D), output shape (max_len, 256)
* LSTM Layer with 128 units
* Dense to 64 with tanh activation function
* Dense to number of classes with softmax function

### Evaluate on test sentences
Again, run your model to predict on the test sentences, you need to do the preprocessing on these sentences first and save your prediction to a list of labels, e.g `[0, 2, 1, 5, ....]`. Then save your prediction as `rnn.p` using the following code and submit to Gradescope.

```python
pickle.dump(test_prediction, open("embedding.p", "wb"))
```
## Part 3: BERT[10 points]
In this part, you will use the BERT pipeline to further improve the performance.
This part is open-ended, we just provide one example of using BERT, feel free to find other tutorial online to customize on this task.

### Hugging Face
We will use the [hugging face](https://huggingface.co/transformers/) backbone for this part. Install the transformaer package using the following command:

```bash
pip3 install transformers
```

Run the following code in python to define the bert tokenizer and bert model.

```python
from transformers import *
from transformers import BertTokenizer, TFBertModel, BertConfig
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased") #feel free to change the model
bert_model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=9)
```
You could change the `"bert-base-uncased"` to any other state-of-art model, [here](https://huggingface.co/models) is the list of all existing models.

### Use BERT Tokenizer to preprocess the data
The BERT Tokenizer will return a dictionary which contains 'input\_ids', 'token\_type\_ids' and 'attention\_mask', we will use the **'input\_ids'** and **'attention\_mask'** later.

```python
# Test the tokenizer
sent = X_train[0]
tokenized_sequence= bert_tokenizer.encode_plus(sent,add_special_tokens = True,
                                              max_length =30,pad_to_max_length = True, 
                                              return_attention_mask = True)
print(tokenized_sequence)
print(bert_tokenizer.decode(tokenized_sequence['input_ids']))
```

Use the bert tokenizer described above, encode the training and validations sentences, note that the max length should be 64. Please complete the `BERT_Tokenizer(sentences)` function which takes in a list of sentences and return two numpy array which represent the **`input_ids`** and **`attention_mask`**.

### Train your model and evaluate on test images
After you preprocessed the data, you could use the given code to run the model. Then just use BERT model to make prediction on the test sentences. Save the prediction as `bert.p`.

```
pickle.dump(test_prediction, open("bert.p", "wb"))
```

### Write your own commands
Please write 10 sentences for each category, this will be very helpful for future students!

```
my_commands = {'no': [], 
               'driving': [], 
               'light': [],
               'head': [],
               'state': [],
               'connection': [], 
               'stance': [], 
               'animation': [],
               'grid': []}
               
pickle.dump(my_commands, open("my_commands.p", "wb"))
```

## Leaderboard
Please use your best model to predict on test sentences and save the prediction as `best.p`, we will give top 1 extra 5 points for this assigenment, top 2-3: 3 points, top 5 - 10: 1 point.

## Submission
Here are what you need to submit for this homework:

* r2d2_hw5.ipynb
* rnn.p
* embedding.p
* bert.p
* best.p (for leaderboard)
* my_commands.p

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
