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

def filter_dict_by(dict, field, value):
    for k in dict.keys():
        if dict[k][field] != value:
            del dict[k]

# questions = dict(clothing=1, construction=12, device=6, food=10, furniture=1, implement=5)
#
#
# chosen = max(questions, key=questions.get)
# del questions[chosen]
# # ret = questions.popitem()
# print chosen