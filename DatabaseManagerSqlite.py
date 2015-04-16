__author__ = 'Khaleeq'

# import pymysql
import sqlite3
import Learner

class DatabaseManager():
    def __init__(self):
        self.all_features = {}
        self.all_concepts = {}
        # connection = pymysql.connect('localhost', 'root', '', 'objectdb');
        connection = sqlite3.connect('data/object_db.sqlite')
        connection.text_factory = str
        cursor = connection.cursor()

        def setupDB():
        # Fetch and store all features from db WHERE wbClass != 'taxonomic'
            cursor.execute(""" SELECT *
                            FROM features
                        """)
            features = cursor.fetchall()

        ### Fetch and store all concepts from db
            cursor.execute(""" SELECT *
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

                new_feat = {feature[0] : dict(brainregion=feature[1], wbclass=feature[2], wbtype=feature[3], isDisting=feature[5], distinctiveness=feature[6], concepts=featCons)}
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



                new_conc = {concept[0] : dict(commonName=concept[1], superclass=concept[2], subclass=concept[3], freq=concept[7],  features=conFeats) }
                self.all_concepts.update(new_conc)

                # print self.all_features["is_a_reptile"]["concepts"]["python"]

                # print table?
                # print len(table)
                # this_feat = Feature(feature[0], feature[1], feature[2], feature[3], conceptTable)
                # self.all_features.append(this_feat)
            # print all_features


        setupDB()


### test
# print("Fetching from Database...")
# # database = DatabaseManager()
# print("Fetch complete. One moment please.");