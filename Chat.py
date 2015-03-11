__author__ = 'Khaleeq'

import re
import nltk
import pprint
from random import shuffle
from collections import deque
from DatabaseManager import DatabaseManager
from Questioner import *
from collections import OrderedDict
from collections import Counter
from numpy import median

D = DatabaseManager()
# global concepts
all_concepts = D.all_concepts
# global features
all_features = D.all_features


artefacts = dict(clothing={}, construction={}, device={}, food={}, furniture={}, implement={})
naturals = dict(animal={}, mineral={}, plant={})
tax = dict(artefact=artefacts, natural=naturals)


def middle(nums):
    nums.sort()
    length = len(nums)
    half = length/2
    # if length % 2:                  #if even, return the half
    return nums [half]
    # else:                            #if odd
    #     return (nums[half] + nums[half-1] )/2

class Chat:
    def __init__(self):
        self


def features_in_objectset(dict):
    cfeats = [] #all concept features
    for c in dict.keys():
        cfeats += all_concepts[c]['features'].keys()
    return Counter(cfeats);


def main():

    concepts = all_concepts # this gets drilled down as it needs to be counted
    features = all_features # this an alais to the full list, as we drill down in the questions instead

    objects = OrderedDict()
    for obj in concepts:
        objects.update({obj: 0})  # Put all objects  into dic with value 0
    # shuffle(objects)
    sorted(objects, key=objects.get, reverse=True)


    sup = superQuestion(tax.keys())
    sub = subQuestion(tax[sup].keys())

    if sub == "skip":
        for k in concepts.keys():
            if concepts[k]['superclass'] != sup:
                del objects[k]

    else:
        for k in concepts.keys():
            if concepts[k]['subclass'] != sub:
                del objects[k]

# CHANGE SO NO DUPES IN THIS LIST

    # for f in features.keys():
    #         if not (f in cfeats):
    #             del features[f]
    #         # filteredFeatures.append(f)
    # # features = filteredFeatures

    # for key in features.keys():
    #     # print "x"
    #     qlen = len(features[key]['concepts'])
    #     questions.update({key: qlen})

          # Put all questions  into dic with number of concepts
        # questions = OrderedDict(sorted(questions.items(), key=lambda t: t[1]))
    # print questions


    answer = ""
    guess = ""
    guessed = False
    numQuestions = 0
    questionHistory = []
    asked = [] #sorta hacky, could access question history directly but this should avoid a loop

    # for s in featStack:
    #     print s.name


    def getQuestion(objects, asked):

        questions = features_in_objectset(objects)
        for q in questions.keys():
            if q in asked:
                del questions[q]
            if not (q in all_features):     ### TODO: Currently HACKY fix to skip unlisted features
                del questions[q]

        # print "queue length is " + str(len(featureQueue))
        # print questions
        # thisQ = questions[0]
        # questions.remove[0]
        # questions = OrderedDict(question)
        # sorted(questions.iteritems(), key=lambda x: x[1])
        # print questions

        counts = sorted(questions.values())
        counts = list(set(counts))         ##try without dupes?
        print counts
        med = int(middle(counts))
        print med
        chosen = [k for k, v in questions.iteritems() if v == med][0] ## TODO some check for closest med if missing key error (though this makes no sense)

        # chosen = max(questions, key=questions.get) #TODO: check if max length?
        # ret = questions.popitem()
        return chosen

        # print questions
        # return thisQ
        # print "queue length is now " + str(len(featureQueue))


    while (not guessed): #and (len(featStack) > 0):
        numQuestions+=1
        question = getQuestion(objects, asked)
        print question + "?" ##needs converting with regex

        #filter affected
        # print all_features.keys()
        affected = all_features[question]['concepts']
        intersection = affected.viewkeys() & objects.viewkeys()
        for o in affected.keys():
            if not (o in intersection):
                del affected[o]

        print affected.keys()


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
                else:
                    objects[o] = objects.get(o) + -1
                    print "\t :" + o + " -1"


        elif answer == "no":
            # print "Oh, must be something else..."
            for o in affected:
                if o in objects.keys():
                    print "\t :" + o + "X"
                    del objects[o]
                    # objects[o] = objects.get(o) - 1
                    # print "\t :" + o + " -1"
                    # if objects.get(o) <= -1:
                    #     del objects[o]
        questionHistory.append({ question : answer } )
        asked.append(question)
        print str(len(objects)) + " objects remain" + "\t" + "current guess: " + max(objects, key=objects.get)

        # win condition
        if len(objects) == 1: # or len(questions) == 0:
            guess = objects.popitem()
            guessed = True

        elif len(objects) == 0:
            lost = True

    if guessed == True:
        print "I guess that the object is: " + str(guess[0]) + " \t Questions: " + str(numQuestions)
        print "Otherwise it might be one of these..."
        print str(objects)
    elif lost == True:
        print "You win!"
         #implement learn new object

if __name__ == "__main__": main()


### things to add
### # simple version: preset questions
### # better version: median based
### # check that guessing object list disjointed with current guesses-answer set (not full object set or just super/subsets) (IMPORTANT as max/median values shouldn't come from to big a group, and questions might be wasted)
### # shortcut for disting feat (remember will be late in game as they only apply to 1. Infact, all disting are 1 or 2, so moot?
### # ask specific question to check top answers (more intelligent to check current guess, which can then be removed)
### # ranking more applicable object features in some way
### # LEARNING
### ## Show changes (new yesses, and possibly different from expected answer (if NO=straight remove is changed)
### # if set to 20, continue option?
### # other win conditions?
### # should no alway remove?
### # back and skip?
### # what if features run out?
### # check for questions with no effect
### # answer error checking
### deal with when there is a limited set of starter features, we only want present features to taken from concepts array