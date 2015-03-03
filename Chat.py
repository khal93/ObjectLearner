__author__ = 'Khaleeq'

import re
import nltk
import pprint
from random import shuffle
from collections import deque
from DatabaseManager import DatabaseManager
from Questioner import *
from collections import OrderedDict

D = DatabaseManager()
# global concepts
all_concepts = D.all_concepts
# global features
all_features = D.all_features


artefacts = dict(clothing={}, construction={}, device={}, food={}, furniture={}, implement={})
naturals = dict(animal={}, mineral={}, plant={})
tax = dict(artefact=artefacts, natural=naturals)


class Chat:
    def __init__(self):
        self


def main():

    concepts = all_concepts
    features = all_features
    sup = superQuestion(tax.keys())
    sub = subQuestion(tax[sup].keys())

    if sub == "skip":
        # close to only sup
        filteredConcepts = concepts.copy()
        for k in concepts.keys():
            if concepts[k]['superclass'] != sup:
                del filteredConcepts[k]
                # print "deletion"
                # filteredConcepts.append(c)
        concepts = filteredConcepts


    else:
        # close down to sub
        filteredConcepts = concepts.copy()
        for k in concepts.keys():
            if concepts[k]['subclass'] != sub:
                del filteredConcepts[k]
                # print "deletion"
                # filteredConcepts.append(c)
        concepts = filteredConcepts

    filteredFeatures = features.copy()


# CHANGE SO NO DUPES IN THIS LIST
    cfeats = []
    for c in concepts.keys():
        cfeats += concepts[c]['features'].keys()
    for f in features.keys():
            if not (f in cfeats):
                del filteredFeatures[f]
            # filteredFeatures.append(f)
    features = filteredFeatures



    questions = {}
    # maxq = 0
    for key in features.keys():
        # print "x"
        qlen = len(features[key]['concepts'])
        questions.update({key: qlen})  # Put all questions  into dic with number of concepts
        # questions = OrderedDict(sorted(questions.items(), key=lambda t: t[1]))
    # print questions


    objects = OrderedDict()
    for obj in concepts:
        objects.update({obj: 0})  # Put all objects  into dic with value 0
    # shuffle(objects)
    sorted(objects, key=objects.get, reverse=True)


    answer = ""
    guess = ""
    guessed = False

    # for s in featStack:
    #     print s.name


    def getQuestion():
        # print "queue length is " + str(len(featureQueue))
        # print questions
        # thisQ = questions[0]
        # questions.remove[0]
        # questions = OrderedDict(question)
        sorted(questions.iteritems(), key=lambda x: x[1])
        ret = questions.popitem()
        return ret[0]

        # print questions
        # return thisQ
        # print "queue length is now " + str(len(featureQueue))


    while (not guessed): #and (len(featStack) > 0):
        question = getQuestion()
        affected = features[question]['concepts']
        print affected
        print question + "?" ##needs converting with regex


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
            # print "Interesting..."
            for o in affected:
                if o in objects.keys():
                  objects[o] = objects.get(o) + 1
                  print "\t :" + o + " +1"

        elif answer == "no":
            # print "Oh, must be something else..."
            for o in affected:
                if o in objects.keys():
                    objects[o] = objects.get(o) - 1
                    print "\t :" + o + " -1"
                    if objects.get(o) <= -1:
                        del objects[o]

        print str(len(objects)) + " objects remain"

        # win condition
        if len(objects) == 1:
            guess = objects.pop()
            guessed = True

    print "I guess that the object is: " + guess
    # print objects
if __name__ == "__main__": main()