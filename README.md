# ObjectLearner
objectlearner

## Work in progress
This is currently a work in progress for my university honours project. Things might change drastically... I don't know!

## How the system should work
Project is to build and evaluate an object learning system with data currently represented in a relational databae. 
The database set up is currently set up with tables for 'concepts' and 'features' with a third table to join these together. 
Features are derived from the McRae norms, which are pretty basic at the moment, but I would hope these would grow as the system learns new ones through natural language. There are some taxonomic features, but these are quite crudely represented at the moment (eg some animals maybe have "is_mammal" but not "is_animal" or vice-versa, some may have neither even if one might apply).

Currently imeplemted a question generation and and object prediction (similar to twenty questions or Akinator), as it generates questions from these features to drill down a list of candidate objects. 
The user then answers yes or no, decreasing the set of possible concepts and generating a new question based on the remaining items. The system would then learn about new objects, and make corrections to its existing dataset. I hope to expand this to allow for ambigious features and a spectrum of answers rather than just the yes-no 
dichotomy. It may possibly even allow for parsing some natural language understanding of more open-ended dialogue. 

The end goal is for a learning system, rather than just a guessing game. The system will learn about new objects and features, as well as correcting it's own data.
