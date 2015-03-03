__author__ = 'Khaleeq'

import re
import nltk
import pprint
from random import shuffle
from collections import deque
from DatabaseManager import DatabaseManager
from Questioner import *

D = DatabaseManager()
featStack = shuffle(D.all_features)
featureQueue = D.all_features

artefacts = dict(clothing={}, construction={}, device={}, food={}, furniture={}, implement={})
naturals = dict(animal={}, mineral={}, plant={})
tax = dict(artefact=artefacts, natural=naturals)

# featureQueuel.sort(lambda x, y: x[1])
#needs SORTING!!!

conceptList = D.all_concepts


# print type(featureQueue)
# length = len(featureQueue)
# print featureQueue[0].name
# print featureQueue[length-1].name

class Chat:
    def __init__(self):
        self


def main():
    # inp = ""
    # while not (inp == "yes" or inp == "no"):
    #     print("Question")
    #     inp = raw_input().lower()
    #  print "Your object is " + inp + "."


    sup = superQuestion(tax.keys())
    sub = subQuestion(tax[sup].keys())

    if sub == "skip":
        # close to only sup
        print "a"
    else:
        # close down to sub
        print "b"


    objects = {}
    for obj in conceptList:
        objects.update({obj.name: 0})  # Put all objects  into dic with value 0

    answer = ""
    guess = ""
    guessed = False

    # for s in featStack:
    #     print s.name


    def getQuestion():
        # print "queue length is " + str(len(featureQueue))
        return featureQueue.pop()
        # print "queue length is now " + str(len(featureQueue))


    while (not guessed): #and (len(featStack) > 0):
        # for feat in featureQueue:
        #     q = feat
        q = getQuestion()
        question = q.name
        positives = q.concepts

        # print question
        # print positives ###### EMPTY??

        print question + "?" ##needs converting with regex
        # print type(positives)
        # print positives

        answer = raw_input().lower()

        # while not (answer == "yes" or answer == "no"):
        #     print question + "?" ##needs converting with regex
        #     answer = raw_input().lower()
            # print answer

            # if answer == "yes":
            #     validInput = True;
            # elif answer == "no":
            #     validInput = True;

        if answer == "yes":
            print "Interesting..."
            for o in positives:
                oname = list(o)[0]
                objects[oname] = objects.get(oname) + 1
                if objects.get(oname) > 2:
                    guess = oname
                    guessed = True
            # print objects

        elif answer == "no":
            print "Oh, must be something else..."
            for o in positives:
                oname = list(o)[0]
                objects[oname] = objects.get(oname) - 1
                if objects.get(oname) <= -1:
                    del objects[oname]
                print len(objects)

    print "I guess that the object is: " + guess
    print objects
if __name__ == "__main__": main()