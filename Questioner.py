__author__ = 'Khaleeq'

# from bintrees import BinaryTree



# tax = BinaryTree()

# tax['artefact'] = 'clothing', 'construction', 'device', 'food', 'furniture', 'implement'
# # print tax
# tax['natural'] = 'animal', 'mineral', 'plant'
# print tax
# print("Is this object:"),
# for key in tax.keys():
#     print(key + " "),
# print "?"

def natLangList(list, terminator):
    retString = ""
    for i in xrange(len(list)):
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

def filterDictBy(dict, field, value):
    for k in dict.keys():
        if dict[k][field] != value:
            del dict[k]

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


def answerCertaintyOld(answer):
    if answer == "yes":
        return 1
    elif answer == "no":
        return -1
    else:
        return 0

def answerCertainty(answer):
    #TODO hacky, order of ifs can mess it up as atm it checks for al substrings not precisely just words.
    ###  TODO Crude implementation for now. In future can find a better way with NLTK?

    score = 0.0

    negation = ["not"]
    no=["no", "false"]
    unlikely=["unlikely", "doubtful", "negative"]
    unsure=["maybe", "don't know", "unsure", "skip", "can't tell", "not relevant", "irrelevant"]
    likely=["likely", "positive", "confident"]
    yes=["yes", "true"]


    if any(word in answer for word in no):
        score = -1

    if any(word in answer for word in unlikely):
        score = -0.5

    if any(word in answer for word in unsure):
        score = 1

    if any(word in answer for word in likely):
        score = 0.5

    if any(word in answer for word in yes):
        score =1

###### NEGATION!
    if any(word in answer for word in negation):
        score = score * -1
    # else:
    #     score = 0

    return score

# questions = dict(clothing=1, construction=12, device=6, food=10, furniture=1, implement=5)
#
#
# chosen = max(questions, key=questions.get)
# del questions[chosen]
# # ret = questions.popitem()
# print chosen