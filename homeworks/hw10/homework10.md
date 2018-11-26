---
layout: default
img: python.jpg
img_link: http://xkcd.com/353/
caption: Hello world!
title: CIS 521 Homework 10 "Extra Credit"
active_tab: homework
release_date: 2018-12-06
due_date: 2018-12-13 23:59:00EDT
materials:
    - 
        name: skeleton file
        url: homework10.py 
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



Homework 10: Extra Credit [? points]
=============================================================

## Instructions

In this assignment, you will get an experience writing functions used in Neural Networks from scratch, as well as using one of the generic machine learning frameworks called [PyTorch](https://pytorch.org). 

A skeleton file [homework10.py](homework10.py) containing empty definitions for each question has been provided. Since portions of this assignment will be graded automatically, none of the names or function signatures in this file should be modified. However, you are free to introduce additional variables or functions if needed.

You will find that in addition to a problem specification, most programming questions also include a pair of examples from the Python interpreter. These are meant to illustrate typical use cases, and should not be taken as comprehensive test suites.

You are strongly encouraged to follow the Python style guidelines set forth in [PEP 8](http://www.python.org/dev/peps/pep-0008/), which was written in part by the creator of Python. However, your code will not be graded for style.

Once you have completed the assignment, you should submit your file on [Gradescope]({{page.submission_link}}).

You may submit as many times as you would like before the deadline, but only the last submission will be saved. 


## Set up Pytorch 

Pytorch is one of the most popular deep learning frameworks in both industry and academia, and learning its use will be invaluable should you choose a career in deep learning. 
You will be using Pytorch for this assignment, and instead of providing you source code, we ask you to build off a couple Pytorch tutorials. 

### Setup

#### Using miniconda
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

## 1. Individual Functions [? points]

In this section, you will ..

1. **[? points]** Write a function `convolve_greyscale(image, filter)` that accepts a greyscale `image` as a numpy array of size `[image_height, image_width]`, and a kernel filter as a numpy array of size `[kernel_height, kernel_width]` and performs a convolution, which consists of adding each element of the image to its local neighbors, weighted by the kernel. The result of this function is a new numpy array that has the same size as `image`. Please apply zero-padding to the input image to calculate image edges. 
        
    ```python
    >>> image = np.array([
            [0,  1,  2,  3,  4],
            [ 5,  6,  7,  8,  9], 
            [10, 11, 12, 13, 14], 
            [15, 16, 17, 18, 19], 
            [20, 21, 22, 23, 24]])
    >>> kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]])
    >>> print(convolve_greyscale(image, kernel))
    [[-6 -3 -1  1  8]
     [ 9  6  7  8 19]
     [19 11 12 13 29]
     [29 16 17 18 39]
     [64 47 49 51 78]]
    ```

   ```python
    >>> image = np.array([
            [0,  1,  2,  3,  4],
            [ 5,  6,  7,  8,  9], 
            [10, 11, 12, 13, 14], 
            [15, 16, 17, 18, 19], 
            [20, 21, 22, 23, 24]])
    >>> kernel = np.array([
            [1, 2, 3],
            [0, 0, 0],
            [-1, -2, -3]])
    >>> print(convolve_greyscale(image, kernel))
    [[  16   34   40   46   42]
     [  30   60   60   60   50]
     [  30   60   60   60   50]
     [  30   60   60   60   50]
     [ -46  -94 -100 -106  -92]]
    ```

3. **[? points]** Write a function `convolve_rgb(image, filter)` that accepts RGB `image` as a numpy array of size `[image_height, image_width, number_of_channels]`, and a kernel filter as a numpy array of size `[kernel_height, kernel_width]` and performs a convolution. You can use `convolve_greyscale(image, filter)` in the previous section. The result of this function is a new numpy array that has the same size as `image`. Please apply zero-padding to the input image to calculate image edges. 

4. **[? points]** Write a function `max_pooling(image, kernel, stride)` that accepts a greyscale `image` as a numpy array of size `[image_height, image_width]`, `kernel` that is a typle `(kernel_height, kernel_width)`, `stride` of pooling window and applies a max pooling operation that reduces the dimensionality of an image. 

    ```python
       >>> image = np.array([
                [1, 1, 2, 4],
                [5, 6, 7, 8],
                [3, 2, 1, 0],
                [1, 2, 3, 4]])
       >>> kernel = (2, 2)
       >>> stride = 2
       >>> print(max_pooling(image, kernel, stride))
       [[6 8]
        [3 4]]
    ```

4. **[? points]** Write a function `average_pooling(image, kernel, stride)` that accepts a greyscale `image` as a numpy array of size `[image_height, image_width]`, `kernel` of `[kernel_height, kernel_width]`, `stride` of pooling window and applies an average pooling operation, instead of maximum.

    ```python
       TODO: Example
    ```

5.  **[? points]** Write a function `sigmoid(x)` that accetps an input `x` and applies a sigmoid activation function. 
  
    ```python
       TODO: Example
    ```

6. **[? points]** Write a function `tanh(x)` that an input `x` and applies a tanh activation function. 

    ```python
       TODO: Example
    ```

## 2. Fashion MNIST Dataset [? points]

A [train dataset](train_dataset.csv) is provided along this Specification, which is adopted from the [Fashion MNIST dataset](https://github.com/zalandoresearch/fashion-mnist). 

1.  **[? points]** Parse the data in `__init__(self, file)` of `MyDataset` class as `self.X` and `self.Y` variables. The first column of the dataset is a label `Y` and the remaining columns correspond to the pixel of an 28*28 image flattened.

    ```python
    >>> my_dataset=MyDataset('train_dataset.csv')
    >>> loader = torch.utils.data.DataLoader(my_dataset, batch_size=100, shuffle=False)
    >>> print(list(loader)[0])
    ?
    ```
2.  **[? points]** Fill in  `__init__(self)` and  `forward(self, x)` of `MyModel` class to implement architecture of your choice. We suggest starting from 1 convolutional layer followed by the final output layers. It is up to you to decide the architecture, and we recommend looking int [`torch.nn.MaxPool2d`](https://pytorch.org/docs/stable/nn.html) and [`torch.nn.Conv2d`](https://pytorch.org/docs/stable/nn.html) functions. 


## 3. Feedback [0 points]

1. **[0 points]** Approximately how long did you spend on this assignment?
2. **[0 points]** Which aspects of this assignment did you find most challenging? Were there any significant stumbling blocks?
3. **[0 points]**  Which aspects of this assignment did you like? Is there anything you would have changed?