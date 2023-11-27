import spacy
import pandas as pd

from nltk import stem

nlp = spacy.load("en_core_web_trf")

def yaniv_bot(irc, msg, sender, channel):
    df_nba = pd.read_csv('nba_data.csv')
    print(df_nba)
    if msg == 'example':
        irc.send(
                channel, f"{sender}: example bot q/a")
        pass
    return

msg = "Who played Golden State on 12/2021"

lemmatizer = stem.WordNetLemmatizer()

doc = nlp(msg)
date = year = month = day = None
verb = None
verb_executor = None
propn = None
for token in doc:
    text, dep, head_text, pos, index = token.text, token.dep_.lower(), token.head.text, token.pos_.lower(), token.i

    if pos == 'num':
        date = text
    if pos == 'verb':
        verb = text
    if dep == 'nsubj' and pos == 'propn':
        verb_executor = text
    if (dep == 'dobj' or dep == 'pobj') and pos == 'propn':
        verb_executor = None
    if pos == 'propn':
        propn = text.lower()

df_nba = pd.read_csv('nba_data.csv')

date_components = date.split('/')
if len(date_components) == 3:
    month, day, year = date_components
    df_nba = df_nba[(df_nba['month'] == int(month)) & (df_nba['day'] == int(day)) & (df_nba['year'] == int(year))]
elif len(date_components) == 2:
    month, year = date_components
    df_nba = df_nba[(df_nba['month'] == int(month)) & (df_nba['year'] == int(year))]
else:
    year = date_components
    df_nba = df_nba[(df_nba['year'] == int(year))]

relevant_nba_data = None
if lemmatizer.lemmatize(verb) in ('beat', 'win', 'won', 'defeated', 'defeat'):
    if verb_executor:
        relevant_nba_data = df_nba[((df_nba['visitor_team'].str.lower().str.contains(propn)) & (df_nba['visitor_team_points'] > df_nba['home_team_points'])) | ((df_nba['home_team'].str.lower().str.contains(propn)) & (df_nba['home_team_points'] > df_nba['visitor_team_points']))]
    else:
        relevant_nba_data = df_nba[((df_nba['visitor_team'].str.lower().str.contains(propn)) & (df_nba['visitor_team_points'] < df_nba['home_team_points'])) | ((df_nba['home_team'].str.lower().str.contains(propn)) & (df_nba['home_team_points'] < df_nba['visitor_team_points']))]
    # return message
elif lemmatizer.lemmatize(verb) in ('lose', 'lost', 'fall', 'fell'):
    if verb_executor:
        relevant_nba_data = df_nba[((df_nba['visitor_team'].str.lower().str.contains(propn)) & (df_nba['visitor_team_points'] < df_nba['home_team_points'])) | ((df_nba['home_team'].str.lower().str.contains(propn)) & (df_nba['home_team_points'] < df_nba['visitor_team_points']))]
    else:
        relevant_nba_data = df_nba[((df_nba['visitor_team'].str.lower().str.contains(propn)) & (df_nba['visitor_team_points'] > df_nba['home_team_points'])) | ((df_nba['home_team'].str.lower().str.contains(propn)) & (df_nba['home_team_points'] > df_nba['visitor_team_points']))]
    # return message
elif lemmatizer.lemmatize(verb) in ('play', 'played'):
    relevant_nba_data = df_nba[df_nba['visitor_team'].str.lower().str.contains(propn) | df_nba['home_team'].str.lower().str.contains(propn)]
else:
    message_content = 'Sorry, I don\'t understand the question :(. Try to rephrase it!'

print(relevant_nba_data)