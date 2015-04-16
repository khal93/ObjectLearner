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

    tops = d.copy()
    avg = np.mean(tops.values())

    for o in tops.keys():
        if (int(tops.get(o)) < avg):# or (o in nots):
            del tops[o]
        # if (len(d) > 0) and (o in nots):
        #      del d[o]
    return tops

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
    # intersection = effected.viewkeys() & objects.viewkeys()
    # for o in effected.keys():
    #     if not (o in intersection):
    #         del effected[o]

    print effected.keys()
    return effected


def learning(objects, guess, history):
    # print str(history)
    # objects = OrderedDict([('fawn', 405.0), ('pigeon', 315.0), ('mackerel', 170.0), ('housefly', 551.66666666666674), ('crocodile', 204.99999999999997), ('seaweed', 273.33333333333337), ('pheasant', 354.99999999999994), ('grape', 84.999999999999972), ('nectarine', 311.66666666666669), ('celery', 110.0), ('cougar', 166.66666666666663), ('penguin', 575.00000000000011), ('minnow', 165.0), ('pumpkin', 173.33333333333334), ('porcupine', 241.66666666666669), ('dandelion', 460.0), ('bear', 143.33333333333329), ('peacock', 545.0), ('asparagus', 205.0), ('emu', 423.33333333333326), ('bison', 91.666666666666657), ('nightingale', 518.33333333333326), ('pineapple', 525.0), ('crow', 311.66666666666669), ('grasshopper', 318.33333333333331), ('vine', 330.0), ('worm', 413.33333333333326), ('lion', 271.66666666666669), ('seal', -93.333333333333343), ('chicken', 488.33333333333326), ('honeydew', 253.33333333333334), ('pine', 333.33333333333337), ('mandarin', 220.0), ('cantaloupe', 236.66666666666669), ('cauliflower', 310.0), ('goldfish', 383.33333333333331), ('bat_(animal)', 230.0), ('tortoise', 91.666666666666686), ('cow', 441.66666666666669), ('pickle', 13.333333333333329), ('hamster', 501.66666666666674), ('eggplant', 178.33333333333331), ('raccoon', 675.0), ('groundhog', 345.0), ('apple', 356.66666666666669), ('coconut', 271.66666666666669), ('starling', 734.99999999999989), ('duck', 288.33333333333337), ('walnut', 291.66666666666669), ('lime', 256.66666666666663), ('alligator', 275.0), ('parsley', 93.333333333333314), ('frog', 416.66666666666663), ('turkey', 143.33333333333334), ('yam', 245.0), ('pearl', 445.0), ('crab', 278.33333333333331), ('blueberry', 233.33333333333331), ('calf', 265.0), ('squid', 166.66666666666663), ('squirrel', 310.0), ('mushroom', 386.66666666666669), ('tiger', 221.66666666666669), ('rabbit', 366.66666666666674), ('bull', 240.0), ('olive', 83.333333333333314), ('coyote', 186.66666666666663), ('swan', 585.0), ('rat', 590.00000000000011), ('cat', 630.0), ('turnip', 380.0), ('robin', 790.0), ('seagull', 555.0), ('pelican', 353.33333333333331), ('prune', 308.33333333333331), ('pony', 458.33333333333326), ('moth', 253.33333333333331), ('dolphin', 96.666666666666657), ('rooster', 343.33333333333331), ('carrot', 341.66666666666663), ('beaver', 173.33333333333326), ('shrimp', 206.66666666666669), ('lamb', 180.0), ('rhubarb', 168.33333333333331), ('mouse', 469.99999999999989), ('stone', 251.66666666666669), ('python', 423.33333333333331), ('catfish', 176.66666666666669), ('elephant', 255.0), ('goat', 398.33333333333331), ('cod', 151.66666666666669), ('moose', 160.0), ('snail', 320.0), ('cranberry', 400.0), ('leopard', 135.0), ('garlic', 353.33333333333331), ('birch', 530.0), ('cabbage', 296.66666666666669), ('hawk', 436.66666666666674), ('dove', 653.33333333333337), ('broccoli', 116.66666666666666), ('sparrow', 756.66666666666652), ('tomato', 95.000000000000028), ('peach', 153.33333333333331), ('platypus', 68.333333333333371), ('giraffe', 356.66666666666663), ('mole_(animal)', 246.66666666666663), ('camel', 351.66666666666657), ('emerald', 343.33333333333337), ('canary', 918.33333333333337), ('iguana', 713.33333333333326), ('elk', -108.33333333333339), ('willow', 235.00000000000006), ('cherry', 400.0), ('avocado', -15.0), ('chickadee', 750.0), ('grapefruit', 273.33333333333331), ('radish', 343.33333333333337), ('orange', 320.0), ('raven', 536.66666666666674), ('budgie', 551.66666666666652), ('vulture', 425.00000000000006), ('salamander', 149.99999999999997), ('gopher', 356.66666666666663), ('caterpillar', 141.66666666666666), ('clam', 176.66666666666671), ('cedar', 308.33333333333331), ('flea', 425.0), ('falcon', 650.0), ('flamingo', 400.0), ('rock', 253.33333333333331), ('butterfly', 330.0), ('hare', 498.33333333333326), ('spider', 600.00000000000011), ('goose', 461.66666666666669), ('lobster', 191.66666666666669), ('zebra', 393.33333333333331), ('eel', 81.666666666666657), ('plum', 225.0), ('fox', 298.33333333333326), ('rattlesnake', 438.33333333333326), ('trout', 345.00000000000006), ('eagle', 541.66666666666663), ('pepper', 400.0), ('salmon', 406.66666666666663), ('corn', 376.66666666666669), ('cockroach', 156.66666666666663), ('raspberry', 145.0), ('walrus', -106.66666666666667), ('raisin', 440.0), ('ostrich', 580.0), ('beans', 311.66666666666669), ('ox', 100.0), ('cucumber', 131.66666666666663), ('octopus', 55.000000000000043), ('owl', 538.33333333333337), ('zucchini', 98.333333333333343), ('wasp', 566.66666666666674), ('chimp', 235.0), ('buzzard', 313.33333333333331), ('lettuce', 238.33333333333331), ('guppy', 241.66666666666669), ('tuna', -115.0), ('sheep', 398.33333333333331), ('horse', 398.33333333333331), ('spinach', 201.66666666666663), ('stork', 578.33333333333326), ('woodpecker', 521.66666666666663), ('banana', 296.66666666666669), ('shell', 318.33333333333331), ('turtle', 348.33333333333331), ('otter', 240.00000000000006), ('beets', 256.66666666666663), ('bluejay', 730.0), ('strawberry', 165.0), ('blackbird', 756.66666666666674), ('hornet', 338.33333333333337), ('whale', 29.999999999999972), ('donkey', 250.0), ('mink', 323.33333333333337), ('perch', 243.33333333333326), ('chipmunk', 460.0), ('beetle', 374.99999999999989), ('deer', 329.99999999999994), ('pig', 298.33333333333326), ('ant', 330.0), ('panther', 420.0), ('oriole', 508.33333333333337), ('hyena', 138.33333333333331), ('lemon', 470.0), ('partridge', 341.66666666666663), ('oak', 236.66666666666663), ('parakeet', 631.66666666666663), ('finch', 741.66666666666674), ('cheetah', 153.33333333333331), ('toad', 286.66666666666669), ('tangerine', 311.66666666666669), ('onions', 478.33333333333331), ('pear', 405.0), ('peas', 211.66666666666666), ('sardine', 153.33333333333331), ('potato', 265.0), ('caribou', 118.33333333333334), ('dog', 530.0), ('gorilla', 168.33333333333334), ('skunk', 608.33333333333326), ('buffalo', -53.333333333333329)])
    guess = "canary"
    history = [{'has_fur': 'no'}, {'is_furry': 'no'}, {'has_seeds': 'no'}, {'it_tastes_good': 'no'}, {'is_a_vegetable': 'no'}, {'is_brown': 'sometimes'}, {'has_4_legs': 'no'}, {'is_white': 'yes'}, {'it_lives_in_water': 'no'}, {'it_sings': 'yes'}, {'has_legs': 'yes'}, {'is_a_mammal': 'no'}, {'has_a_tail': 'yes'}, {'has_eyes': 'yes'}, {'is_green': 'no'}, {'is_hunted_by_people': 'no'}, {'is_edible': 'no'}, {'is_an_insect': 'no'}, {'it_lives_on_farms': 'no'}, {'is_grey': 'no'}, {'it_swims': 'no'}, {'it_lays_eggs': 'yes'}, {'it_builds_nests': 'yes'}, {'is_a_pet': 'yes'}, {'is_hard': 'no'}, {'is_large': 'no'}, {'is_yellow': 'yes'}]

    print "What is this object called?"
    name = raw_input().lower()
    if object in objects.keys():
        ##TODO NLTK check for synonyms as well
        print "Is it: " + str(objects[name])

        ##print table of matches??

        ##Ask about discrepancies??
        ##Ask to compare current object with guessed object
        ##Update current object (and guessed object?) in DB
    else:
        print "I think this is a new object"
        ##Ask to compare current object with guessed object
        ##Ask some more questions?
        ##Add new object to DB


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

            qConcepts = all_features[question]["concepts"]

            effected = getEffected(objects, question)

            #TODO NORMALISE SCORE WITH RELEVANCE-RATING
            num = 0
            for o in objects.keys():
                num = num +1
            # if objects.get(o) <= -2:
            #     removeObject(objects, o)
                featureConfidence = 0

                if o in effected:
                  agreement = qConcepts[o]["agreementScore"]
                  freq = qConcepts[o]["frequency"]
                  featureConfidence = agreement / freq
                  # modifyScore(objects, o, + certainty)
                  modifyScore(objects, o,  (100 * np.mean([certainty, featureConfidence])))
                  if certainty < 0:
                      currentlyNot.append(o)
                else:
                  # modifyScore(objects, o, - certainty)
                  modifyScore(objects, o, ( 0 - (100* np.mean([certainty, featureConfidence]) )))
                  # if certainty > 0:
                  #   currentlyNot.append(o)
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

            print str(num) + " out of " + str(len(objects)) + " changed"


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

        #TODO: - check for clear winner, something better than difference 100?
        remObjs = objects.copy()
        del remObjs[topGuess]

        # if len(topObjects(objects, [])) == 1:
        if len (bestCandidates) == 1:
            readyToGuess = True

        if  len(remObjs) == 0:
            readyToGuess == True
        else:
            secondGuess = max(remObjs, key=remObjs.get)
            if objects[topGuess] - objects[secondGuess] >= 100:
                readyToGuess = True

        print str(len(bestCandidates)) + " candidates" + "\t" + "current guess: " + topGuess + " (" + str(objects[topGuess]) + ")"


        # win condition
        if readyToGuess == True: # or len(questions) == 0:
            guess = max(objects, key=objects.get)
            print "I predict that the object is: " + guess[0] + " \t " + str(guess)
            print "\n Questions asked: " + str(numQuestions)
            print str(questionHistory)

            print "\n Objs: "
            print str(objects)

            # guessed = True
            print "Is this correct?"
            isCorrect = raw_input().lower()

            if isCorrect == "no":
                lost = True

        elif len(objects) == 0: #TODO??
            lost = True

    # if guessed == True:

    if lost == True:
        print "You win!"
         #implement learn new object
        # learning(objects, guess, questionHistory)





def main():

    # concepts = all_concepts # this gets drilled down as it needs to be counted
    # features = all_features # this an alias to the full list, as we drill down in the questions instead
    #
    # print type(all_features)
    # print str(all_features)
    # print "\n /n \n"
    # print type(all_concepts)
    # print str(all_concepts)

    print (all_concepts)

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