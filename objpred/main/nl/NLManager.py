from __future__ import division


__author__ = 'Khaleeq'

import csv
import numpy as np
from collections import OrderedDict
from collections import Counter
from objpred.functional import ConceptGuessing, QuestionGeneration
import objpred.functional.FeatLearning as FeatLearning

from objpred.misc.AllConstants import *
from nltk.corpus import wordnet as wn
from prettytable import PrettyTable
from objpred.misc.MyLoggers import *


NUM_CAN_GRAPH = []
EACH_GUESS = []
EACH_RUNNER = []
MID_GRAPH = []
DIFF_GRAPH = []
SCORE_HISTORY = []
VALID_ANS = []
INVALID_ANS = []

# logger.debug("Y")
# logger.info("X")
logger.debug("++++++++++++++++++++++++++++ NEW NAT LANG RUN ++++++++++++++++++++++++++++++++++++")

from objpred.main.nl.db.DbManager import DatabaseManager
all_concepts = {}
all_features = {}


logger.info("One moment please. Fetching from Database...")
D = DatabaseManager()
D.setupDb()

all_concepts = D.all_concepts
all_features = D.all_features

wns = wn.synsets("thing")


### Types for pre-question

class Main:
    def __init__(self):
        self




def setupObjects(all_concepts):
    objDict = OrderedDict()
    for obj in all_concepts:
        objDict.update({obj: 0.0})  # Put all objects  into dic with value 0
    # shuffle(objects)
    # shuffle(objects)
    # sorted(objects, key=objects.get, reverse=True)
    return objDict

def playGame():

    # D.setupDb()
    #
    # all_concepts = D.all_concepts
    # all_features = D.all_features

    concepts = all_concepts
    logger.info("Please think of an object... \n")

    objects = setupObjects(all_concepts)
    kind = QuestionGeneration.askPreQuestions(concepts, objects)
    # kind = "unknown"

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
    secondGuess =""

            ##answer processing

    def processAnswer_priorty(question, answer, mid):
    ### Changes prioty depending on answers
        certainty = FeatLearning.answerCertainty(answer)
        currentlyNot = []

        qConcepts = all_features[question]["concepts"]

        effected = ConceptGuessing.getBasicEffected(objects, question, all_features, all_concepts)

        #TODO NORMALISE SCORE WITH RELEVANCE-RATING
        num = 0
        for o in objects.keys():
            num = num +1
        # if objects.get(o) <= -2:
        #     removeObject(objects, o)
            featureConfidence = 0.5

            if o in effected:
              agreement = qConcepts[o]["agreementScore"]
              freq = qConcepts[o]["frequency"]
              featureConfidence = agreement / freq
              # modifyScore(objects, o, + certainty)
              mod = (100 * np.mean([certainty, featureConfidence]))
              ConceptGuessing.modifyScore(objects, o,  mod)
              # if mod < 0:
              #     currentlyNot.append(o)
              #     logger.info("X IS NOT::" + str(o)
            else:
              # modifyScore(objects, o, - certainty)

              mod = ( 0 - (100* np.mean([certainty, featureConfidence]) ))
              ConceptGuessing.modifyScore(objects, o, mod)
              # if mod > 0:
              #   currentlyNot.append(o)
              #   logger.info("Y IS NOT::" + str(o)

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

        # logger.info('\t [' + str(num) + " out of " + str(len(objects)) + " changed. ]" #TODO counts out of total

    while (not readyToGuess): #and (len(featStack) > 0):
        numQuestions+=1
        bestCandidates = ConceptGuessing.topObjects(objects, currentlyNot)
        # logger.info(str(bestCandidates)
        qmid = QuestionGeneration.getQuestion(bestCandidates, asked, all_concepts, all_features)
        question = qmid['question']
        mid = qmid['mid']
        MID_GRAPH.append(mid) #TODO LOGSTORE


        validResponse = ""
        while validResponse == "":
            logger.info(QuestionGeneration.convertToQuestion(question))
            response = raw_input().lower()
            logger.debug(">>>" + response)

            validResponse = validationRe(response, VALID_INPUT)
            if validResponse == 'valid':

                    ######
                    VALID_ANS.append(response)
                    response = FeatLearning.scoreToAnswer(FeatLearning.answerCertainty(response))
                    logger.info(">>> interpreted as \"" + response +"\"")
                    processAnswer_priorty(question, response, mid)
                    questionHistory.append({ question : response } )
                    asked.append(question)

                    # logger.info(str(len(objects)) + " objects remain" + "\t" + "current guess: " + max(objects, key=objects.get))
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
                        diff = objects[topGuess] - objects[secondGuess]
                        # logger.debug(str(diff)+"::diff") ##TODO LOG THIS
                        DIFF_GRAPH.append(diff) #TODO LOGSTORE

                        if diff >= 150:
                            readyToGuess = True

                    topCount = objects.values().count(objects[topGuess])
                    if topCount == 1: #TODO LOG THIS UNPRINT
                        logger.info(">>> [ BEST GUESS: " + topGuess + " (" + str(objects[topGuess]) + ") ]  /  [ " +str(len(bestCandidates)) + "/" + str(len(objects)) + " candidates" + " ]")
                    else:
                        logger.info(">>> [ BEST GUESS: Undecided  (" + str(topCount) + " items at " + str(objects[topGuess]) + ") ]  /  [ " +str(len(bestCandidates))  + "/" + str(len(objects)) +  " candidates" + " ]")
                    # print "[ Looking at " +str(len(bestCandidates)) + "/" + str(len(objects)) + " possible candidates" + " ]"

                    NUM_CAN_GRAPH.append(len(bestCandidates)) #TODO LOGSTORE
                    EACH_GUESS.append({topGuess: str(objects[topGuess])})
                    EACH_RUNNER.append({secondGuess: str(objects[secondGuess])})
                    ####

            else:
                INVALID_ANS.append(response)
                logger.info("Sorry I didn't get that.")


        #filter effected
        # logger.info(all_features.keys()





        # processAnswer_y1_nX()
        # processAnswer_mirror()




        # win condition
        if readyToGuess == True: # or len(questions) == 0:
            guess = max(objects, key=objects.get)
            guessName = all_concepts[guess]["commonName"]
            alts = []

            for w in wn.synset(guess).lemma_names():
                if w != guessName:
                        alts.append(w.replace("_"," "))

            logger.info("I have guessed " + guessName + ".")

            guessTable = PrettyTable(["Object", "Definition", "Questions asked"])
            guessTable.align["Definition"] = "l"
            define =  wn.synset(guess).definition()
            if len(alts) > 0:
                define += "\n (" + QuestionGeneration.natLangList(alts, "&") +")"
            guessTable.add_row([guessName.title(), define, str(numQuestions)])
            # logger.info(guessTable
            logger.info(guessTable)



            # if alts logger.info("Alternatively known as " + natLangList(alts, "&")
            # logger.info("\n Questions asked: " + str(numQuestions) #TODO LOG THIS
            logger.info(str(questionHistory))
                # logger.info(str(objects)

            # guessed = True

            isValid = ""
            while isValid == "":
                logger.info("Is this correct?")
                input = raw_input().lower()
                logger.debug(">>>" + input)
                isValid = branchingValidation(input, POS, NEG)
                if isValid == 'neg':
                    lost = True

             #implement learn new object

            logger.debug("Guessed correctly?::" + str(not lost))

            learnResults = FeatLearning.learning(guess, secondGuess, questionHistory, all_concepts, lost)
            answers =learnResults['answers']
            learnId = learnResults['learnt']


            newFeatsGuess = learnResults['newFromGuess']
            newFeatsLearn = learnResults['newFromLearn']

            updatedFromGuess = learnResults['existGuess']
            updatedFromLearn = learnResults['existLearn']

            amendedFeats = learnResults['amendments']

            if not (learnId in all_concepts.keys()):
                D.insertNewConcept(learnId, kind=kind)
                commonName = learnId.split('.')[0]
            else:
                commonName = all_concepts[learnId]["commonName"]

            D.updateConceptFeature(answers,learnId)
            logger.info("Updated database for "+ commonName)
            printEndLogCSV(topGuess, secondGuess, objects, questionHistory, lost, learnId, answers, newFeatsGuess,newFeatsLearn, updatedFromGuess, updatedFromLearn, amendedFeats)




def main():

    AskToGuess()

def printEndLogCSV(topGuess, secondGuess, objectScores, questions, lost, learnId, answers, newFeatsGuess, newFeatsLearn, updatedFromGuess, updatedFromLearn, amendedFeats):

    filepath = '../logs/natlang1.csv'


    if learnId in objectScores.keys():
        learnScore = objectScores[learnId]
    else:
        learnScore = "X"

    if topGuess in objectScores.keys():
        topScore = objectScores[topGuess]
    else:
        topScore = "X"

    if secondGuess in objectScores.keys():
        secondScore = objectScores[secondGuess]
    else:
        secondScore = "X"
    f1=csv.writer(open(filepath, 'a'))
    f1.writerow([str(SUBJECT_ID), str(learnId), str(learnScore), str(topGuess),  str(topScore),  str(secondGuess),
                 str(secondScore), str(not lost), str(len(questions)), str(NUM_CAN_GRAPH), str(EACH_GUESS) , str(EACH_RUNNER),
                 str(MID_GRAPH), str(Counter(VALID_ANS)), str(Counter(INVALID_ANS)), str(objectScores),
                 str(newFeatsGuess), str(newFeatsLearn), str(updatedFromGuess), str(updatedFromLearn), str(amendedFeats),
                 str(DIFF_GRAPH), str(questions), str(answers)
     ])

    del NUM_CAN_GRAPH[:]
    del EACH_GUESS[:]
    del EACH_RUNNER[:]
    del MID_GRAPH[:]
    del DIFF_GRAPH[:]
    del SCORE_HISTORY[:]
    del VALID_ANS[:]
    del INVALID_ANS[:]

def AskToGuess(first=True):
    isValid = ""
    while isValid == "":
        if not first:
            logger.info("Would you like to try again with another object?")
            again = raw_input().lower()
            logger.debug(">>>" + again)
            isValid = branchingValidation(again, POS, NEG)
            if isValid == 'pos':
                logger.info("One moment please, fetching from database...")
                playGame()
                AskToGuess(first=False)
            elif isValid == 'neg':
                logger.info("Okay, thank you for playing.")
        else:
            playGame()
            AskToGuess(first=False)




if __name__ == "__main__": main()




