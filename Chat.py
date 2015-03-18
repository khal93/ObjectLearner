__author__ = 'Khaleeq'

import re
# import nltk
import pprint
from random import shuffle
from collections import deque
from DatabaseManager import DatabaseManager
from Questioner import *
from collections import OrderedDict
from collections import Counter

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


def featuresInObjectset(dict):
    cfeats = [] #all concept features
    for c in dict.keys():
        cfeats += all_concepts[c]['features'].keys()
    return Counter(cfeats);


def askPreQuestions(concepts, objects):
    sup = superQuestion(tax.keys())
    for k in concepts.keys():
            if concepts[k]['superclass'] != sup:
                del objects[k]


    # sub = subQuestion(tax[sup].keys())
    # if sub == "skip":
    #     for k in concepts.keys():
    #         if concepts[k]['superclass'] != sup:
    #             del objects[k]
    #
    # else:
    #     for k in concepts.keys():
    #         if concepts[k]['subclass'] != sub:
    #             del objects[k]

            # CHANGE SO NO DUPES IN THIS LIST

            # for f in features.keys():
            # if not (f in cfeats):
            #             del features[f]
            #         # filteredFeatures.append(f)
            # # features = filteredFeatures

            # for key in features.keys():
            #     # print "x"
            #     qlen = len(features[key]['concepts'])
            #     questions.update({key: qlen})

            # Put all questions  into dic with number of concepts
            # questions = OrderedDict(sorted(questions.items(), key=lambda t: t[1]))



def getQuestion(objects, asked):

    # Get questions over remaining objects
    questions = featuresInObjectset(objects)

    # Remove previously asked and unlisted questions
    for q in questions.keys():
        if q in asked:
            del questions[q]
        if not (q in all_features):     ### TODO: Currently HACKY fix to skip unlisted features
            del questions[q]

##DIVIDE AND CONQUER##
    # Counts of related objects for each feat
    counts = sorted(questions.values())
    counts = list(set(counts))         ##conversion removes duplicates

    # Find median/middle count value, and use this to select a question
    med = int(middle(counts))
    chosen = [k for k, v in questions.iteritems() if v == med][0]
    return chosen

    # chosen = max(questions, key=questions.get) #TODO: separate out maxed/standard q version
    # ret = questions.popitem()


def setupObjects():
    objDict = OrderedDict()
    for obj in all_concepts:
        objDict.update({obj: 0})  # Put all objects  into dic with value 0
    # shuffle(objects)
    # sorted(objects, key=objects.get, reverse=True)
    return objDict

def modifyScore(d, key, value):
    if key in d.keys():
        if isinstance( value, ( int, long ) ):
            d[key] = d.get(key) + value
        print "\t :" + key + " +" + str(value)

def removeObject(d, key):
    del d[key]
    print "\t :" + key + " X"



def playGame(concepts, features):
    objects = setupObjects()
    askPreQuestions(concepts, objects)



    #initialise blank response and guess
    response = ""
    guess = ""
    guessed = False
    numQuestions = 0
    questionHistory = []
    asked = [] #sorta hacky, could access question history directly but this should avoid a loop

    # for s in featStack:
    #     print s.name



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


        response = raw_input().lower()

        ##answer processing

        def processAnswer_priorty():
        ### Changes prioty depending on answers
        ###TODO: Currently removes at -2, as prioritised version still to be done
            if response == "yes":
                for o in objects.keys():
                    if objects.get(o) <= -2:
                        removeObject(objects, o)
                    if o in affected:
                      modifyScore(objects, o, +1)
                    else:
                      modifyScore(objects, o, int(0-1))


            elif response == "no":
                for o in objects.keys():
                    if objects.get(o) <= -2:
                        removeObject(objects, o)
                    if o in affected:
                      modifyScore(objects, o, int(0-1))
                    else:
                        modifyScore(objects, o, 1)



        def processAnswer_mirror():
        ###Yes: +1 or remove  /  No: remove or +1
            if response == "yes":
                for o in objects.keys():
                    if o in affected:
                      modifyScore(objects, o, 1)
                    else:
                        removeObject(objects, o)

            elif response == "no":
                for o in objects.keys():
                    if o in affected:
                        removeObject(objects, o)
                    else:
                        modifyScore(objects, o, 1)

        def processAnswer_y1_nX():
        ### Yes: +1 / No: Remove
            if response == "yes":
                for o in affected:
                    if o in objects.keys():
                      modifyScore(objects, o, 1)
                    # else:
                    #     removeObject(objects, o)

            elif response == "no":
                for o in affected:
                    if o in objects.keys():
                        removeObject(objects, o)
                    # else:
                    #     modifyScore(objects, o, 1)


        # processAnswer_y1_nX()
        # processAnswer_mirror()
        processAnswer_priorty()


        questionHistory.append({ question : response } )
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
        # print "Otherwise it might be one of these..."
        # print str(objects)
    elif lost == True:
        print "You win!"
         #implement learn new object




def main():

    # concepts = all_concepts # this gets drilled down as it needs to be counted
    # features = all_features # this an alias to the full list, as we drill down in the questions instead

    playGame(all_concepts, all_features)


if __name__ == "__main__": main()


### things to add
### # simple version: preset questions
### # better version: median based
### # check that guessing object list disjointed with current guesses-answer set (not full object set or just super/subsets) (IMPORTANT as max/median values shouldn't come from to big a group, and questions might be wasted)
### # shortcut for disting feat (remember will be late in game as they only apply to 1. Infact, all disting are 1 or 2, so moot?
### # TODO??? ask specific question to check top answers (more intelligent to check current guess, which can then be removed)
### # ranking more applicable object features in some way
### # TODO LEARNING
### ## TODO Show changes (new yesses, and possibly different from expected answer (if NO=straight remove is changed)
### # if set to 20, continue option?
### # TODO other win conditions?
### # should no alway remove?
### # TODO back and skip?
### # what if features run out?
### # check for questions with no effect
### # answer error checking