import os
import spacy
import pandas as pd

from nltk import stem

directory = os.path.dirname(os.path.realpath(__file__))

nlp = spacy.load("en_core_web_trf")
df_nba = pd.read_csv(directory + '/' + 'nba_data.csv')
nba_team_names = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
                  'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
                  'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
                  'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
                  'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
                  'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
lemmatizer = stem.WordNetLemmatizer()

def yaniv_bot(irc, msg, sender, channel):
    if 'nba:' not in msg:
        return

    global df_nba

    doc = nlp(msg)
    date = year = month = day = None
    verb = None
    verb_executor = None
    propn = None
    for token in doc:
        text, dep, head_text, pos, index = token.text, token.dep_.lower(), token.head.text, token.pos_.lower(), token.i

        if pos == 'num' or (pos in ('propn', 'noun') and not text.isalpha()):
            date = text
        if pos == 'verb':
            verb = text
        if dep == 'nsubj' and pos in ('propn', 'noun'):
            verb_executor = text
        if (dep == 'dobj' or dep == 'pobj') and pos in ('propn', 'noun') and text.isalpha():
            verb_executor = None
        if pos in ('propn', 'noun') and text.isalpha():
            propn = text.lower()

    if propn is None:
        return

    team_name = [name for name in nba_team_names if propn in name.lower()]
    if not team_name:
        return

    team_name = team_name[0]
    date_components = date.split('/')
    preposition = 'in' if len(date) == 4 else 'on'
    if len(date_components) == 3:
        month, day, year = date_components
        df_dates = df_nba[(df_nba['month'] == int(month)) & (df_nba['day'] == int(day)) & (df_nba['year'] == int(year))]
    elif len(date_components) == 2:
        month, year = date_components
        df_dates = df_nba[(df_nba['month'] == int(month)) & (df_nba['year'] == int(year))]
    else:
        year = date_components
        df_dates = df_nba[(df_nba['year'] == int(year))]

    message_content = ''
    relevant_nba_data = None
    if lemmatizer.lemmatize(verb) in ('beat', 'win', 'won', 'defeated', 'defeat'):
        if verb_executor:
            relevant_nba_data = df_dates[((df_dates['visitor_team'].str.contains(team_name)) & (df_dates['visitor_team_points'] > df_dates['home_team_points'])) | ((df_dates['home_team'].str.contains(team_name)) & (df_dates['home_team_points'] > df_dates['visitor_team_points']))]

            if len(relevant_nba_data) == 0:
                message_content = f'It appears that the {team_name} didn\'t win any games {preposition} {date}.\n'
            else:
                for index, row in relevant_nba_data.iterrows():
                    message_content += f"{row['home_team']} ({int(row['home_team_points'])}) - {row['visitor_team']} ({int(row['visitor_team_points'])})\n"

                message_content = f'The {team_name} won {len(relevant_nba_data)} game(s) {preposition} {date}. The opponents and final scores were:\n' + message_content
        else:
            relevant_nba_data = df_dates[((df_dates['visitor_team'].str.contains(team_name)) & (df_dates['visitor_team_points'] < df_dates['home_team_points'])) | ((df_dates['home_team'].str.contains(team_name)) & (df_dates['home_team_points'] < df_dates['visitor_team_points']))]

            if len(relevant_nba_data) == 0:
                message_content = f'It appears that the {team_name} didn\'t lose any games {preposition} {date}.\n'
            else:
                for index, row in relevant_nba_data.iterrows():
                    message_content += f"{row['home_team']} ({int(row['home_team_points'])}) - {row['visitor_team']} ({int(row['visitor_team_points'])})\n"

                message_content = f'The {team_name} lost {len(relevant_nba_data)} game(s) {preposition} {date}. The opponents and final scores were:\n' + message_content

    elif lemmatizer.lemmatize(verb) in ('lose', 'lost', 'fall', 'fell'):
        if verb_executor:
            relevant_nba_data = df_dates[((df_dates['visitor_team'].str.contains(team_name)) & (df_dates['visitor_team_points'] < df_dates['home_team_points'])) | ((df_dates['home_team'].str.contains(team_name)) & (df_dates['home_team_points'] < df_dates['visitor_team_points']))]

            if len(relevant_nba_data) == 0:
                message_content = f'It appears that the {team_name} didn\'t lose any games {preposition} {date}.\n'
            else:
                for index, row in relevant_nba_data.iterrows():
                    message_content += f"{row['home_team']} ({int(row['home_team_points'])}) - {row['visitor_team']} ({int(row['visitor_team_points'])})\n"

                message_content = f'The {team_name} lost {len(relevant_nba_data)} game(s) {preposition} {date}. The opponents and final scores were:\n' + message_content
        else:
            relevant_nba_data = df_dates[((df_dates['visitor_team'].str.contains(team_name)) & (df_dates['visitor_team_points'] > df_dates['home_team_points'])) | ((df_dates['home_team'].str.contains(team_name)) & (df_dates['home_team_points'] > df_dates['visitor_team_points']))]

            if len(relevant_nba_data) == 0:
                message_content = f'It appears that the {team_name} didn\'t win any games {preposition} {date}.\n'
            else:
                for index, row in relevant_nba_data.iterrows():
                    message_content += f"{row['home_team']} ({int(row['home_team_points'])}) - {row['visitor_team']} ({int(row['visitor_team_points'])})\n"

                message_content = f'The {team_name} won {len(relevant_nba_data)} game(s) {preposition} {date}. The opponents and final scores were:\n' + message_content

    elif lemmatizer.lemmatize(verb) in ('play', 'played'):
        relevant_nba_data = df_dates[df_dates['visitor_team'].str.contains(team_name) | df_dates['home_team'].str.contains(team_name)]

        if len(relevant_nba_data) == 0:
            message_content = f'It appears that the {team_name} didn\'t play {preposition} {date}. Please ask another question!\n'
        else:
            win_count = lose_count = 0
            for index, row in relevant_nba_data.iterrows():
                message_content += f"{row['home_team']} ({int(row['home_team_points'])}) - {row['visitor_team']} ({int(row['visitor_team_points'])})\n"
                if row['home_team'] == team_name and row['home_team_points'] > row['visitor_team_points']:
                    win_count += 1
                elif row['visitor_team'] == team_name and row['visitor_team_points'] > row['home_team_points']:
                    win_count += 1
                else:
                    lose_count += 1

            message_content = f'The {team_name} played {len(relevant_nba_data)} game(s) {preposition} {date}. They won {win_count} game(s) and lost {lose_count} game(s) during this time. The final scores were:\n' + message_content
    else:
        message_content = 'Sorry, I don\'t understand your question :(. Please try to rephrase it!\n'

    for line in message_content.split('\n')[:-1]:
        irc.send(channel, f"{sender}: {line}")
    return