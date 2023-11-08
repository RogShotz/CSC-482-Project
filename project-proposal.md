# Project Proposal
## Names, Majors, and Years
Luke Rowe, CSC, Grad Student

Jeremiah Lee, CSC, 5th-Year

Brandon Kwe, CSC, Grad Student

Yaniv Sagy, CSC, 4th-Year

## Geneology Extractor
We thought that this project sounded interesting.
Some of the challenges that could we think could come about from this project are detection of the speaker, whether they are a character or simply a third person, and detection of the relationships when speaking as a third or first person.
One major component we would like to propose is tagging the speaker for sentences like "He is my brother" or general context queues.
In and of itself, this will be a sub-problem of the project we need to pursue in order to find a lot of the relations.
Most texts are not like genesis 5 in the old testement so we will need to use this speaker tagging.
As a first goal we would aim to extract the explicitly stated relationships, like in genesis 5.
We all felt that this project would engage us and would be a great problem to solve so we would really enjoy having this for our project.

## Data Plan
To begin, we plan on gathering data from Wikipedia. Many Wikipedia articles on individual contain a "Personal Life" section which often contains familial relationships. We could scrape Wikipedia for these sections and label them with what relationships they contain, which could then be used to train a model for outputting familial relationships in text. This model could be tested with data from Wikidata which would allow us to download the information in a machine-parsable format like JSON. If we manage to get a model working well with this data, we could then move to something more difficult like novels where relationships are often not as explicitly stated and the number of family members in the family tree would be significantly greater.

## Possible System Design
![System Design](Diagram.drawio.png)

## Preliminary Tools and Libraries
Spacy or NLTK to do tokenization and handle input string.
A ML model, yet to be determined. Could be NLTK's built in ML functionality or another library like scikit-learn like PyTorch.
Probably Python JSON for testing with data from WikiData.


## Backup Projects We Would Also Enjoy
- QA system about CSSE

- CPE departments Artificial CSC Student
