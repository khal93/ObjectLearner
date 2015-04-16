__author__ = 'Khaleeq'


import Guesser
import random
from collections import Counter


tax = ["artefact", "natural"]

def natLangList(list, terminator):
    retString = ""
    for i in xrange(len(list)):
        if len(list) == 1:
            return list[0]
        if i == len(list) -1:
            retString += str(" " +terminator + " " + list[i])
        elif i == 0:
            retString += str((list[i]))
        else:
            retString += str(", " + list[i])
    return retString


def superQuestion(list):
    print("Is this object an"),
    print(natLangList(list, "or")),
    print "?"

    answer = raw_input().lower()
    # print list
    if answer not in list:
        superQuestion(list)
        # print "not"
    else:
        # print "is in"
        return answer

def subQuestion(list):
    # print list
    print("Is it a kind of "),
    print(natLangList(list, "or")),
    print "?"
    answer = raw_input().lower()

    print answer
    # print list
    if answer in list:
        return answer
    else:
        return "skip"


def askPreQuestions(concepts, objects):
    sup = superQuestion(tax)
    for k in concepts.keys():
            if concepts[k]['superclass'] != sup:
                del objects[k]



def featuresInObjectset(dict, all_concepts):
    cfeats = [] #all concept features
    for c in dict.keys():
        cfeats += all_concepts[c]['features'].keys()
    return Counter(cfeats);



def getQuestion(objects, asked, all_concepts, all_features):

    # Get questions over remaining objects
    questions = featuresInObjectset(objects, all_concepts)

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
    med = int(Guesser.middle(counts))
    questionChoices = [k for k, v in questions.iteritems() if v == med]
    return random.choice(questionChoices)

    # chosen = max(questions, key=questions.get) #TODO: separate out maxed/standard q version
    # ret = questions.popitem()

def convertToQuestion(feature):

    if feature.startswith('it_'):
        question = feature.replace("it_", "This_object_", 1)
    elif feature.startswith('has_'):
        question = feature.replace("has_", "Does_it_have_", 1)
    elif feature.startswith('is_'):
        question = feature.replace("is_", "Is_it_", 1)
    elif feature.startswith('was_'):
        question = feature.replace("was_", "Was_it_", 1)
    elif feature.startswith('it\'s_'):
        question = feature.replace("it's_", "Is_it's_", 1)
    elif feature.startswith('for_example_'):
        question = feature.replace("for_example_", "Is_\"")
        question += "\"_an_example_or_version_of_this_object"
    else:
        pass

    question = question.replace("_", " ")
    question += "?"

    return question

