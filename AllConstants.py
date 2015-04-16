__author__ = 'Khaleeq'

# CONS = {}
# CONS['NEGATION'] = ("not")
# CONS['NO']=("no", "false")
# CONS['UNLIKELY']=("<", "unlikely", "doubtful", "negative")
# CONS['NEUTRAL']=("?", "maybe", "unknown" "don't know", "unsure", "skip", "can't tell", "cannot tell", "irrelevant", "n/a", "does not apply", "", " " )
# CONS['LIKELY']=(">", "likely", "positive", "confident")
# CONS['YES']=("yes", "true")
#
# CONS['POS'] = CONS['YES'] + CONS['LIKELY']
# CONS['NEG'] = CONS['NO'] + CONS['UNLIKELY']
# CONS['VALID_INPUT'] = CONS['POS'] + CONS['NEG'] + CONS['NEUTRAL']

NEGATION = ("not")
NO=("no", "false")
UNLIKELY=("<", "unlikely", "doubtful", "negative")
NEUTRAL=("?", "maybe", "sometimes", "partially", "somewhat", "unknown", "do not know", "undecided", "indefinite", "uncertain", "undetermined", "don't know", "unsure", "skip", "can't tell", "cannot tell", "irrelevant", "n/a", "does not apply", "", " " )
LIKELY=(">", "likely", "positive", "confident")
YES=("yes", "true")

POS = YES + LIKELY
NEG = NO + UNLIKELY
VALID_INPUT = POS + NEG + NEUTRAL


def branchingValidation(input, pos, neg):
    if input in pos:
        return "pos"
    elif input in neg:
        return "neg"
    else:
        return ""

def validation(input, valids):
    if input in valids:
        return "valid"
    else:
        return ""

