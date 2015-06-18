from __future__ import division
# This must be the first statement before other statements.
# You may only put a quoted or triple quoted string,
# Python comments or blank lines before the __future__ line.


__author__ = 'Khaleeq'

# import nltk
import csv
from objpred.functional import ConceptGuessing, QuestionGeneration
import objpred.functional.FeatLearning as FeatLearning
from collections import OrderedDict
from collections import Counter
from objpred.misc.AllConstants import *
from nltk.corpus import wordnet as wn
from prettytable import PrettyTable
from objpred.misc.MyLoggers import *

import numpy as np
from objpred.main.basic.db.BasicDatabaseManagerSqlite import DatabaseManager


NUM_CAN_GRAPH = []
EACH_GUESS = []
EACH_RUNNER = []
MID_GRAPH = []
VALID_ANS = []
INVALID_ANS = []


logger.debug("++++++++++++++++++++++++++++ NEW NAT LANG RUN ++++++++++++++++++++++++++++++++++++")


OBJS_LEFT = []
all_concepts = {}
all_features = {}


logger.info("One moment please. Fetching from Database...")
D = DatabaseManager()
D.setupDb()
all_concepts = D.all_concepts
all_features = D.all_features
###
wns = wn.synsets("thing")




class Main:
    def __init__(self):
        self




def setupObjects(all_concepts):
    objDict = OrderedDict()
    for obj in all_concepts:
        objDict.update({obj: 0.0})  # Put all objects  into dic with value 0    # sorted(objects, key=objects.get, reverse=True)
    return objDict

def playGame(concepts, features):

    concepts = all_concepts
    logger.info("Please think of an object... \n")
    objects = setupObjects(all_concepts)
    kind = QuestionGeneration.askPreQuestions(concepts, objects)    # ects)

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

    def processAnswer_mirror(question, response):
    ###Yes: +1 or remove  /  No: remove or +1

        qConcepts = all_features[question]["concepts"]
        effected = ConceptGuessing.getBasicEffected(objects, question, all_features)

        if response == "yes":
            for o in objects.keys():
                if o in effected:
                  ConceptGuessing.modifyScore(objects, o, 1)
                # else:
                #     Guesser.modifyScore(objects, o, -1)

                #     Guesser.removeObject(objects, o)

        elif response == "no":
            for o in objects.keys():
                if o in effected:
                  ConceptGuessing.modifyScore(objects, o, -1)
                # else:
                #       Guesser.modifyScore(objects, o, 1)

                #     Guesser.modifyScore(objects, o, 1)

    def processAnswer(question, response):
    ### Yes: +1 / No: Remove
        effected = ConceptGuessing.getBasicEffected(objects, question, all_features)
        for o in objects.keys():
            if response == "yes":
                if o in effected:
                  ConceptGuessing.modifyScore(objects, o, 1)
                else:
                    ConceptGuessing.modifyScore(objects, o, -1)

            elif response == "no":
                if o in effected:
                  ConceptGuessing.modifyScore(objects, o, -1)
                else:
                  ConceptGuessing.modifyScore(objects, o, 1)

            if objects.get(o) < np.percentile(objects.values(),75):
                ConceptGuessing.removeObject(objects, o)


    while (not readyToGuess) and (len(objects) > 0):
        numQuestions+=1
        # logger.info(str(objects)
        qmid = QuestionGeneration.getQuestion(objects, asked, all_concepts, all_features)
        question = qmid['question']

        mid = qmid['mid']
        MID_GRAPH.append(mid) #TODO LOGSTORE

        validResponse = ""
        while validResponse == "":
            logger.info(QuestionGeneration.convertToQuestion(question))
            response = raw_input().lower()
            logger.debug(">>>" + response)

            validResponse = validation(response, ['yes', 'no', 'y', 'n'])
            if validResponse == 'valid':

                    ######
                    VALID_ANS.append(response)
                    logger.info(">>> interpreted as \"" + FeatLearning.scoreToAnswer(FeatLearning.answerCertainty(response))+"\"")
                    processAnswer(question, response)
                    questionHistory.append({ question : response } )
                    asked.append(question)

                    # logger.info(str(len(objects)) + " objects remain" + "\t" + "current guess: " + max(objects, key=objects.get))
                    if len(objects) == 0:
                        lost == True
                    elif len(objects) > 0:
                        topGuess = max(objects, key=objects.get)
                        topName = all_concepts[topGuess]["commonName"]


                        remObjs = objects.copy()
                        del remObjs[topGuess]
                        if len(remObjs) > 0:
                            secondGuess = max(remObjs, key=objects.get)
                            secondName = all_concepts[secondGuess]["commonName"]
                        else:
                            secondGuess = "NONE"

                        # if len(topObjects(objects, [])) == 1:
                        OBJS_LEFT.append(len(objects))
                        if len (objects) ==1:
                            readyToGuess = True

                        # half = (int(len(objects))//2)
                        # if len(OBJS_LEFT) > 10:
                        #     if len(objects) == OBJS_LEFT[-10]:
                        #         readyToGuess = True
                        #     # print '::'+str(OBJS_LEFT[-2])

                        if len(objects) == 2:
                            logger.info(">>> [ " +str(len(objects)) + " candidates remaining. Top candidates at " + str(objects[topGuess]) + " ("+ topName +", "+ secondName+ "]")

                        if len(objects) > 2:
                            logger.info(">>> [ " +str(len(objects)) + " candidates remaining. Top candidates at " + str(objects[topGuess]) + " ("+ topName +", "+ secondName+ ", ... )]")


                        # print "[" +str(len(objects)) + " candidates remain" + " ]"

                        NUM_CAN_GRAPH.append(len(objects)) #TODO LOGSTORE
                        EACH_GUESS.append({topGuess: str(objects[topGuess])})
                        # EACH_RUNNER.append({secondGuess: str(objects[secondGuess])})
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




            isValid = ""
            while isValid == "":
                logger.info("Is this correct?")
                input = raw_input().lower()
                logger.debug(">>>" + input)
                isValid = branchingValidation(input, POS, NEG)
                if isValid == 'neg':
                    lost = True

            logger.debug("Guessed correctly?::" + str(not lost))
            logger.info(str(questionHistory))


             #implement learn new object
            # learning(guess, secondGuess, questionHistory, all_concepts, lost)
            if lost:
                logger.info("I'm a afraid I couldn't guess your object.")
                # logger.info(str(questionHistory))
                logger.info("What was your object?")
                learnId = raw_input().lower()

                names = []
                for c in all_concepts:
                    n = all_concepts[c]["commonName"]
                    names.append(n)

                if learnId not in names:
                    logger.info("I don't know anything about \"" + learnId + "\".")

            else:
                learnId = all_concepts[topGuess]["commonName"]
            printEndLogCSV(topGuess, secondGuess, objects, questionHistory, lost, learnId, questionHistory)





def main():

    AskToGuess()


def printEndLogCSV(topGuess, secondGuess, objectScores, questions, lost, learnId, questionHistory):



    filepath = '../logs/basic1.csv'


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


    answers = dict((k,v) for d in questionHistory for (k,v) in d.items())

    f1=csv.writer(open(filepath, 'a'))
    f1.writerow([str(SUBJECT_ID), str(learnId), str(learnScore), str(topGuess),  str(topScore),  str(secondGuess),
                 str(secondScore), str(not lost), str(len(questions)), str(NUM_CAN_GRAPH), str(EACH_GUESS) , str(EACH_RUNNER),
                 str(MID_GRAPH), str(Counter(VALID_ANS)), str(Counter(INVALID_ANS)), str(objectScores), str(answers)
    ])

    del NUM_CAN_GRAPH[:]
    del EACH_GUESS[:]
    del EACH_RUNNER[:]
    del MID_GRAPH[:]
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
                playGame(all_concepts, all_features)
                AskToGuess(first=False)
            elif isValid == 'neg':
                logger.info("Okay, thank you for playing.")
        else:
            playGame(all_concepts, all_features)
            AskToGuess(first=False)




if __name__ == "__main__": main()




