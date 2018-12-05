---
layout: default
img: python.jpg
img_link: http://xkcd.com/353/
caption: Hello world!
title: CIS 521 Homework 10 "Extra Credit - Part 2"
active_tab: homework
release_date: 2018-12-10
due_date: 2018-12-17 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: homework10.py 
    - 
        name: dataset.csv
        url: dataset.csv 
submission_link: https://www.gradescope.com/courses/21105
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



Homework 10: Extra Credit [100 points]
=============================================================

## <a name="instructions"></a> Instructions


The [first part](#part_1) of this assignment involves implementing functions commonly used in Neural Networks from scratch without use of external libraries/packages other than [NumPy](http://www.numpy.org).

The [second part](#part_2)of the assignment involves building a Neural Network using one of the Machine Learning frameworks called [PyTorch](https://pytorch.org) for a [Fashion MNIST dataset](https://github.com/zalandoresearch/fashion-mnist).

A skeleton file [homework10.py](homework10.py) containing empty definitions for each question has been provided. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed.

A file containing a sub-set of the Fashion MNIST dataset dataset [dataset.csv](dataset.csv) is provided. 

You will find that in addition to a problem specification, most programming questions also include a pair of examples from the Python interpreter. These are meant to illustrate typical use cases, and should not be taken as comprehensive test suites.

You are strongly encouraged to follow the Python style guidelines set forth in [PEP 8](http://www.python.org/dev/peps/pep-0008/), which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}).

You may submit as many times as you would like before the deadline, but only the last submission will be saved. 



## <a name="part_2"></a> Part 2 [55 points]

The goal of this part of the assignment is to get familiar with one of the Machine Learning frameworks called [PyTorch](https://pytorch.org). 

The installation instructions can be found [here](https://pytorch.org/get-started/locally/). If you are having difficulty installing it here is an alternative way to  [setup PyTorch using miniconda](#setup).


### <a name="setup"></a>  (Setup PyTorch using miniconda)
Miniconda is a package, dependency and environment management for python (amongst other languages). It lets you install different versions of python, different versions of various packages in different environments which makes working on multiple projects (with different dependencies) easy.

There are two ways to use miniconda,

1. **Use an existing installation from another user (highly recommended)**: On ```biglab```, add the following line at the end of your ```~/.bashrc``` file.
```
export PATH="/home1/m/mayhew/miniconda3/bin:$PATH"
```
Then run the following command
```
source ~/.bashrc
```
If you run the command ```$ which conda```, the output should be ```/home1/m/mayhew/miniconda3/bin/conda```.

2. **Installing Miniconda from scratch**: On ```biglab```, run the following commands. Press Enter/Agree to all prompts during installation.
```
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ chmod +x Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh
```
After successful installation, running the command ```$ which conda``` should output ```/home1/m/$USERNAME/miniconda3/bin/conda```.



### Fashion MNIST Dataset


The [dataset.csv](dataset.csv) we will use is a sub-set of the Fashion MNIST dataset . 


<p align="center">
<img src="fashion-mnist-sprite.png" class="img-responsive" width="50%" height="50%"/>
</p>

<p align="center">
<img src="embedding.gif" class="img-responsive" width="50%" height="50%"/>
</p>

The dataset contains 28x28 greyscale images, where each image has a label from one of 10 classes:

| Label | Description |
| --- | --- |
| 0 | T-shirt/top |
| 1 | Trouser |
| 2 | Pullover |
| 3 | Dress |
| 4 | Coat |
| 5 | Sandal |
| 6 | Shirt |
| 7 | Sneaker |
| 8 | Bag |
| 9 | Ankle boot |




#### Part 2.1 [5 points]

Parse the data in `__init__(self, file_path)` of `MyDataset` class as `self.X` and `self.Y` variables. 
The shape of `self.X` is supposed to be (?, 1, 28, 28) and `self.Y` is supposed to be (?,). Each line in the file corresponds 
to a label and an image, where label is in first column and the remaining columns (pixel 1...pixel 784) are image pixels.  
You should expect something as follows when dataset is loaded:

```python
>>> import matplotlib.pyplot as plt
>>> classes = ['T-Shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
>>> dataset = MyDataset('dataset.csv')
>>> print(dataset.X.shape)
(?, 1, 28, 28)
>>> print(dataset.Y.shape)
(?, )
>>> index = 0
>>> print(classes[dataset.Y[index]])
Pullover
>>> image = dataset.X[index]
>>> print(image.shape)
(1, 28, 28)
>>> plt.imshow(image.reshape(28, 28), cmap='gray')
>>> plt.title(classes[dataset.Y[index])
>>> plt.show()
```
<p align="center">
<img src="sample_image.png" class="img-responsive" width="50%" height="50%"/>
</p>


    
#### Part 2.2 [50 points]

Fill in  `__init__(self)` and  `forward(self, x)` of `MyModel` class to implement architecture of your choice. 

We suggest starting from a Fully-Connected Network with a single hidden layer and developing your implementation to a Convolutional Neural Network. You can see performance of different architectures for this dataset [here](https://github.com/zalandoresearch/fashion-mnist/blob/master/README.md#Benchmark)
 
There are many tutorials online for you to use, for instance here [blog post](http://adventuresinmachinelearning.com/pytorch-tutorial-deep-learning/) that builds a Fully-Connected Network with 2 hidden layers. 

We provide code used for training, so your output should be something like:
```text
Epoch : 1/5, Iteration : 100/?,  Loss: 0.4771
Epoch : 1/5, Iteration : 200/?,  Loss: 0.3591
...
Epoch : 5/5, Iteration : ?/?,  Loss: 0.3591
```

You will be evaluated on the reserved test dataset in terms of Accuracy and F1-score. 


## 3. Feedback [0 points]

1. **[0 points]** Approximately how long did you spend on this assignment?
2. **[0 points]** Which aspects of this assignment did you find most challenging? Were there any significant stumbling blocks?
3. **[0 points]**  Which aspects of this assignment did you like? Is there anything you would have changed?