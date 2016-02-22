# Object Prediction and Semantic Feature Learning Through Natural Language Interaction
There have recently been great strides in interactive technologies which emulate the human senses. Machines can now both ‘see’ and ‘speak’. But will machines ever be able to interact with the world in the same way we do? One goal towards achieving a more human experience is for machines to be able to identify and differentiate between real-world objects. 

My fourth year honours project aims to design, build and evaluate an object learning system with limited natural language understanding of user answers. The basic system is somewhat inspired by guessing games such as "20 Questions" and Akinator.

The system includes a basic text-based dialogue system which asks questions based on specific semantic functional features in order to make the most 'educated‘ guess at the given object. This initial 'knowledge' is based on  a set of semantic feature norms from [McRae et al. (2005)](https://7eb9e8e9-a-62cb3a1a-s-sites.googlegroups.com/site/kenmcraelab/publications/McRae_etal_norms_BRM_05.pdf?attachauth=ANoY7croB531J71LKMCVCpl7gGvmPRAav96chD6qbzJtVPRik7ASOJGDmNYE3FAZ_hs3axsJ7wpbvFNQFpWTTEBgIms9bqv5lgeqsIvi0tY5eBmBQL2l6VS5hd5WEkNT3k0qQXdbfm1vYMRyFyVg9Xuqo4gEUJpADwYl9NntCDS_YYCGDy_TMsRHFRKrfBtbscl1hbR62MQt9Z65q6w36WSaVs8EhTtBCh0-Q4AVnAA_lcbVRZ8nafYrePs7IRdbp9L7Dqu55rmL&attredirects=1) and is currently represented in an SQLite relational database. The system is able to generate appropriate questions for guessing and attempts to learn from limited user interaction based on the user's confidence of their answers. This learning faciliates two primary aims, namely (1) to expand and improve its existing knowledge of the concept object, and (2) using this improved knowledge to make better predictions in future.


## Objectives
* Predict a concept from semantic knowledge
* Interpret and evaluate user responses
* Testing predictions by asking the user questions
* Learning to improve future accuracy
