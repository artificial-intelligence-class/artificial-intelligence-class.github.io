############################################################
# CIS 521: R2D2-Homework 4
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

from pymagnitude import *
import numpy as np
import re

############################################################
# Helper Functions
############################################################

def loadTrainingSentences(file_path):
    commandTypeToSentences = {}

    with open(file_path, 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            if len(line.strip()) == 0 or "##" == line.strip()[0:2]:
                continue
            commandType, command = line.split(' :: ')
            commandType = commandType[:-9]
            if commandType not in commandTypeToSentences:
                commandTypeToSentences[commandType] = [command]
            else:
                commandTypeToSentences[commandType].append(command)

    return commandTypeToSentences

############################################################
# Section 3: Intent Detection
############################################################

# Change this path to the location of your magnitude file
path = "/Volumes/SD/hw4_2019/vectors/"
vectors = Magnitude(path + "GoogleNews-vectors-negative300.magnitude")

def sentenceToWords(sentence):
    pass

def cosineSimilarity(vector1, vector2):
    pass

def calcSentenceEmbedding(sentence):
    pass

def sentenceToEmbeddings(commandTypeToSentences):
    '''Returns a tuple of sentence embeddings and an index-to-(category, sentence)
    dictionary.

    Inputs:
        commandTypeToSentences: A dictionary in the form returned by
        loadTrainingSentences. Each key is a string '[category]' which
        maps to a list of the sentences belonging to that category.

    Let m = number of sentences.
    Let n = dimension of vectors.

    Returns: a tuple (sentenceEmbeddings, indexToSentence)
        sentenceEmbeddings: A mxn numpy array where m[i:] containes the embedding
        for sentence i.

        indexToSentence: A dictionary with key: index i, value: (category, sentence).
    '''
    pass

def closestSentence(sentence, sentenceEmbeddings):
    '''Returns the index of the closest sentence to the input, 'sentence'.

    Inputs:
        sentence: A sentence

        sentenceEmbeddings: An mxn numpy array, where m is the total number
        of sentences and n is the dimension of the vectors.

    Returns:
        an integer i, where i is the row index in sentenceEmbeddings 
        that contains the closest sentence to the input
    '''
    pass

def getCategory(sentence, file_path):
    '''Returns the supposed category of 'sentence'.

    Inputs:
        sentence: A sentence

        file_path: path to a file containing r2d2 commands

    Returns:
        a string 'command', where 'command' is the category that the sentence
        should belong to.
    '''
    pass

def accuracy(training_file_path, dev_file_path):
    '''Returns the accuracy of your implementation of getCategory

    Inputs:
        training_file_path: path to training set

        dev_file_path: path to development set

    Let c = number of correctly categorized sentences in the development set.
    Let s = total number of sentences in the development set.

    Returns:
        A float equal to c/s.
    '''
    pass

############################################################
# Section 4: Slot filling
############################################################

def lightParser(command):
    '''Slots for light command
    The slot "lights" can have any combination of "front"/"back"
    '''
    slots = {"holoEmit": False, "logDisp": False, "lights": [], "add": False, "sub": False, "off": False, "on": False}

    ### YOUR CODE HERE ###

    return slots

def directionParser(command):
    '''Slots for directional command
    Directions should support sequential directional commands in one sentence, such as "go straight and turn left". 
    You may ignore special cases such as "make a left before you come back"
    '''
    slots = {"increase": False, "decrease": False, "directions": []}

    ### YOUR CODE HERE ###

    return slots


############################################################
# Section XXX: Feedback
############################################################

# Please let us know how many hours you spent on this assignment (approximate is fine).
feedback_question_1 = 0

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
