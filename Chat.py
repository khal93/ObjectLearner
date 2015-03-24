from __future__ import division
__author__ = 'Khaleeq'

import re
# import nltk
import pprint
import random
from collections import deque
from DatabaseManagerSqlite import DatabaseManager
from Questioner import *
from collections import OrderedDict
from collections import Counter
import numpy as np

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
    half = length//2
    # if length % 2:                  #if even, return the half
    print half
    return nums[half]
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
    questionChoices = [k for k, v in questions.iteritems() if v == med]
    return random.choice(questionChoices)

    # chosen = max(questions, key=questions.get) #TODO: separate out maxed/standard q version
    # ret = questions.popitem()


def setupObjects():
    objDict = OrderedDict()
    for obj in all_concepts:
        objDict.update({obj: 0.0})  # Put all objects  into dic with value 0
    # shuffle(objects)
    # shuffle(objects)
    # sorted(objects, key=objects.get, reverse=True)
    return objDict

def topObjects(d, nots):

    avg = np.mean(d.values())

    for o in d.keys():
        if (int(d.get(o)) < avg) or (o in nots):
            del d[o]
        # if (len(d) > 0) and (o in nots):
        #      del d[o]
    return d

def modifyScore(d, key, value):
    if key in d.keys():
        if isinstance( value, ( int, long, float ) ):
            d[key] = d.get(key) + value
        print "\t :" + key + " +" + str(value) + "\t : "+ str(d.get(key))

def removeObject(d, key):
    del d[key]
    print "\t :" + key + " X"

def getEffected(objects, question):
    effected = all_features[question]['concepts']
    intersection = effected.viewkeys() & objects.viewkeys()
    for o in effected.keys():
        if not (o in intersection):
            del effected[o]

    print effected.keys()
    return effected



def playGame(concepts, features):
    objects = setupObjects()
    askPreQuestions(concepts, objects)



    #initialise blank response and guess
    response = ""
    guess = ""
    readyToGuess = False
    guessed = False
    lost = False
    numQuestions = 0
    questionHistory = []
    asked = [] #sorta hacky, could access question history directly but this should avoid a loop
    currentlyNot = []
    # for s in featStack:
    #     print s.name



        # print questions
        # return thisQ
        # print "queue length is now " + str(len(featureQueue))


    while (not readyToGuess): #and (len(featStack) > 0):
        numQuestions+=1
        bestCandidates = topObjects(objects, currentlyNot)
        # print str(bestCandidates)
        question = getQuestion(bestCandidates, asked)
        print convertToQuestion(question)

        #filter effected
        # print all_features.keys()



        response = raw_input().lower()

        ##answer processing

        def processAnswer_priorty(question, answer):
        ### Changes prioty depending on answers
            certainty = answerCertainty(answer)
            currentlyNot = []


            effected = getEffected(objects, question)

            #TODO NORMALISE SCORE WITH RELEVANCE-RATING
            for o in objects.keys():
            # if objects.get(o) <= -2:
            #     removeObject(objects, o)
                featureConfidence = 0

                if o in effected:
                  featureConfidence = all_features[question]["concepts"][o] / 30
                  # modifyScore(objects, o, + certainty)
                  modifyScore(objects, o,  (100 * np.mean([certainty, featureConfidence])))
                  if certainty < 0:
                      currentlyNot.append(o)

                else:
                  # modifyScore(objects, o, - certainty)
                  modifyScore(objects, o, ( 0 - (100* np.mean([certainty, featureConfidence]) )))
                  if certainty > 0:
                    currentlyNot.append(o)
            #
            # if certainty > 0:
            #     for o in objects.keys():
            #         # if objects.get(o) <= -2:
            #         #     removeObject(objects, o)
            #         if o in effected:
            #           modifyScore(objects, o, +1)
            #         else:
            #           modifyScore(objects, o, int(0-1))
            #
            #
            # elif response == "no":
            #     for o in objects.keys():
            #         # if objects.get(o) <= -2:
            #         #     removeObject(objects, o)
            #         if o in effected:
            #           modifyScore(objects, o, int(0-1))
            #         else:
            #             modifyScore(objects, o, 1)



        # def processAnswer_mirror():
        # ###Yes: +1 or remove  /  No: remove or +1
        #     if response == "yes":
        #         for o in objects.keys():
        #             if o in effected:
        #               modifyScore(objects, o, 1)
        #             else:
        #                 removeObject(objects, o)
        #
        #     elif response == "no":
        #         for o in objects.keys():
        #             if o in effected:
        #                 removeObject(objects, o)
        #             else:
        #                 modifyScore(objects, o, 1)
        #
        # def processAnswer_y1_nX():
        # ### Yes: +1 / No: Remove
        #     if response == "yes":
        #         for o in effected:
        #             if o in objects.keys():
        #               modifyScore(objects, o, 1)
        #             # else:
        #             #     removeObject(objects, o)
        #
        #     elif response == "no":
        #         for o in effected:
        #             if o in objects.keys():
        #                 removeObject(objects, o)
        #             # else:
        #             #     modifyScore(objects, o, 1)


        # processAnswer_y1_nX()
        # processAnswer_mirror()
        processAnswer_priorty(question, response)


        questionHistory.append({ question : response } )
        asked.append(question)

        # print str(len(objects)) + " objects remain" + "\t" + "current guess: " + max(objects, key=objects.get)
        topGuess = max(objects, key=objects.get)

        #TODO: - check for clear winner, something better than difference 5?
        remObjs = objects.copy()
        del remObjs[topGuess]

        if len(bestCandidates) == 1:
            readyToGuess = True

        if  len(remObjs) == 0:
            readyToGuess == True
        else:
            secondGuess = max(remObjs, key=remObjs.get)
            if objects[topGuess] - objects[secondGuess] >= 50:
                readyToGuess = True

        print str(len(bestCandidates)) + " candidates" + "\t" + "current guess: " + topGuess + " (" + str(objects[topGuess]) + ")"


        # win condition
        if readyToGuess == True: # or len(questions) == 0:
            guess = objects.popitem()
            print "I predict that the object is: " + guess[0]
            print "\n Questions asked: " + str(numQuestions)
            # guessed = True

        elif len(objects) == 0: #TODO??
            lost = True

    # if guessed == True:

    if lost == True:
        print "You win!"
         #implement learn new object




def main():

    # concepts = all_concepts # this gets drilled down as it needs to be counted
    # features = all_features # this an alias to the full list, as we drill down in the questions instead
    #
    # print type(all_features)
    # print str(all_features)
    # print "\n /n \n"
    # print type(all_concepts)
    # print str(all_concepts)


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