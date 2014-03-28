from __future__ import division
import sys
import pickle
from collections import defaultdict
from scipy import stats
import math

goodAnswers = "QuestionsAnswers/word_relationship.answers"
#givenAnswers = "precomputedAnswers/testCristinaPearsonCorrelation.answered"
#givenAnswers = "precomputedAnswers/testCristinaEuclideanDistance.answered"
#givenAnswers = "precomputedAnswers/testCristinamanhattanSimilarity.answered"
givenAnswers = "precomputedAnswers/testCristinaSpearmanCorrelation.answered"

# Written by Remi
# Approved and edited by Anouk (made all words lower case)
def load_GivenAnswers(filename):
    f = open(filename, 'r')
    c = [ l.lower().replace("\n","") for l in f.readlines()]
    f.close()
    return c

def load_ExpectedAnswers(filename):
    f = open(filename, 'r')
    c = [ l.lower().replace("\n","").split(" ")[1] for l in f.readlines()]
    f.close()
    return c


if __name__ == "__main__":
    print "Loading given answers..."
    answersGiven = load_GivenAnswers(givenAnswers)
    print answersGiven[0]
    print "Loading the expected answers"
    answersExpected = load_ExpectedAnswers(goodAnswers)
    print answersExpected[0]
    print "Computing accuracy"
    correctAnswers = 0
    
    if(len(answersGiven) == len(answersExpected)):
        for i in range(len(answersGiven)):
            if(answersGiven[i] == answersExpected[i]):
                correctAnswers = correctAnswers + 1
    accuracy = correctAnswers/len(answersGiven) * 100
    print "Accuracy is"
    print accuracy
                    
