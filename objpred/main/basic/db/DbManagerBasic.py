__author__ = 'Khaleeq'

# import pymysql
import sqlite3

import objpred.functional.FeatLearning as FeatLearning
from objpred.misc.MyLoggers import *


class DbManagerBasic():

    def setupDb(self):
        cursor = self.cursor
    # Fetch and store all features from db WHERE wbClass != 'taxonomic'
        cursor.execute(""" SELECT *
                        FROM features
                    """)
        features = cursor.fetchall()

    ### Fetch and store all concepts from db
        cursor.execute(""" SELECT conceptId, commonName, class
                        FROM concepts
                    """)
        concepts = cursor.fetchall()
        # print str(features)

    ### Store all features on an array of Features
        for feature in features:
            # print feature[0]
            cursor.execute("SELECT cf.conceptId, cf.agreementScore, cf.frequency"
            + " FROM features AS f, concept_features AS cf"
            + " WHERE f.featureId = \"" + feature[0] + "\""
            + " AND cf.featureId = f.featureId")

            fc = cursor.fetchall()
            featCons = dict()
            for i, val in enumerate(fc):
                featCons[val[0]] = {'agreementScore' : val[1], 'frequency' : val[2]}
            # featCons = dict(map(list, cursor.fetchall()))

            new_feat = {feature[0] : dict(brainregion=feature[1], wbclass=feature[2], wbtype=feature[3], concepts=featCons)}
            self.all_features.update(new_feat)
            # print type(self.all_concepts)


        # for concept in concepts:

    ### Get subfeatures for each concept, then store each conept as an array of Concepts
        for concept in concepts:
            cursor.execute("SELECT cf.featureId, cf.agreementScore, cf.frequency"
                        + " FROM concepts AS c, concept_features AS cf"
                        + " WHERE c.conceptId = \"" + concept[0] + "\""
                        + " AND cf.conceptId = c.conceptId")
            cf = cursor.fetchall()
            conFeats = dict()
            for i, val in enumerate(cf):
                conFeats[val[0]] = {'agreementScore' : val[1], 'frequency' : val[2]}

            # print str(conFeats)
            # conFeats = dict(map(list, cursor.fetchall()))



            new_conc = {concept[0] : dict(commonName=concept[1], superclass=concept[2], features=conFeats) }
            self.all_concepts.update(new_conc)

            # print self.all_features["is_a_reptile"]["concepts"]["python"]

            # print table?
            # print len(table)
            # this_feat = Feature(feature[0], feature[1], feature[2], feature[3], conceptTable)
            # self.all_features.append(this_feat)
        # print all_features

    def insertNewConcept(self, conId, kind="unknown", name=None):
        if name == None:
            name = conId.split('.')[0]
        statement = 'INSERT INTO concepts (conceptId,commonName, class) VALUES ( "' + conId + '" , "' +  name + '" , "' +  kind + '")'
        # print statement
        self.cursor.execute(statement)
        self.connection.commit()

    def updateConceptFeature(self, answers, concept):
        for feature in answers:
            agreement = str(FeatLearning.answerCertainty(answers[feature]))
            statement = """INSERT OR REPLACE INTO concept_features(cfId, conceptId, featureId, agreementScore, frequency)
		              VALUES (
		                    COALESCE((SELECT cfId FROM concept_features WHERE conceptId =\'""" + concept + """\' AND featureId =\'""" + feature + """\' ) , null),
		                    \'""" + concept + """\',
		                    \'""" + feature + """\',
		                    COALESCE((SELECT agreementScore FROM concept_features WHERE conceptId = \'""" + concept + """\' AND featureId = \'""" + feature + """\') + \'""" + agreement + """\', \'""" + agreement + """\'),
		                    COALESCE((SELECT frequency FROM concept_features WHERE conceptId = \'""" + concept + """\' AND featureId = \'""" + feature + """\') + 1, '1')
		                  );"""
            logger.debug("updated " + concept+"::"+feature)
            self.cursor.execute(statement)
            self.connection.commit()



    def __init__(self):
        self.all_features = {}
        self.all_concepts = {}
        # connection = pymysql.connect('localhost', 'root', '', 'objectdb');
        self.connection = sqlite3.connect('../../data/basic_object_db.sqlite')
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        self.setupDb()


### test
# print("Fetching from Database...")
# database = DatabaseManager()
# database.insertNewConcept("id200", "something200")
# answers = {'has_fur': 'no', 'is_furry': 'yes', 'has_seeds': 'likely', 'it_tastes_good': 'unlikely', 'is_a_vegetable': 'sometimes', 'is_a_bird' : 'yes'}
# concept = "canary.n.04"
# database.updateConceptFeature(answers, concept)


# print("Fetch complete. One moment please.");
