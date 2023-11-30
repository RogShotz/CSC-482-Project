from IRC import IRC
import sys
import time
import random
from phase_3.luke_bot import luke_bot
from phase_3.yaniv_bot import yaniv_bot
from phase_3.brandon_bot import brandon_bot
from phase_3.jeremiah_bot import jeremiah_bot

# IRC Config
server = "irc.libera.chat" 	# Provide a valid server IP/Hostname
port = 6667
channel = "#CSC482b"
botnick = "pog-bot2"
botnickpass = ""		# in case you have a registered nickname
botpass = ""			# in case you have a registered bot
states = ['START',  # 1 indicates first bot speaker, 2 indicates second bot speaker
          '1_INITIAL_OUTREACH',
          '1_SECONDARY_OUTREACH',
          '1_GIVEUP_FRUSTRATED',
          '1_INQUIRY',
          '1_INQUIRY_REPLY',
          '2_OUTREACH_REPLY',
          '2_INQUIRY',
          '2_GIVEUP_FRUSTRATED',
          '2_INQUIRY_REPLY',
          'END']


def main():
    irc = IRC()
    irc.connect(server, port, channel, botnick, botpass, botnickpass)
    start_time = time.time()
    state = states[0]
    convo_target = ''

    while True:
        print('waiting...', end='')
        text = irc.get_response(4)
        sender, m_type, m_tar, msg = response_filter(text)
        # Timer must go before rejection so that it is being updated per timeout as well.
        if msg == 'dev-pass':
            print(f'passed: {state}')
        if time.time() - start_time >= 15:
            if state == 'START':  # For targetting a person for conversation.
                u_list = []
                while not u_list: # run until a good user list is returned
                    u_list = user_list(irc).split(', ')
                    u_list.remove(botnick)

                convo_target = random.choice(u_list)
                irc.send(channel, f"{convo_target}: Hello :)")
                state = states[1]
            elif state == states[1]:
                irc.send(channel, f"{convo_target}: You there? ;(")
                state = states[2]
            elif state == states[2] or state == states[4] or state == states[6] or state == states[7]:
                irc.send(
                    channel, f"{convo_target}: Fine, I didn't wanna talk anyways :(")
                state = states[3]
            elif state == states[3] or state == states[5]:
                state = 'START'  # reset
            start_time = time.time()
        if not sender:  # If the result of response_filter gives None it was no good.
            print('rejected')
            continue

        if msg != 'dev-pass':
            print(f'accepted: {msg}')

        # Bot is talker 1.
        if (msg == 'hi' or msg == 'hello') and state == states[0]:
            convo_target = sender
            speech_choice = random.choice(['hi', "hello back at you!"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            state = states[6]
            start_time = time.time()
        elif (msg == 'how are you?' or msg == "what's happening?") and state == states[6]:
            speech_choice = random.choice(["I'm good", "I'm fine"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            speech_choice = random.choice(["how about you?", "and yourself?"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            state = states[7]
            start_time = time.time()
        elif (msg == "i'm good" or msg == "i'm fine, thanks for asking") and state == states[7]:
            state = states[5]
            start_time = time.time()
        # Bot is talker 2.
        elif (msg == 'hello back at you!' or msg == 'hi') and states.index(state) <= 2:
            speech_choice = random.choice(
                ['how are you?', "what's happening?"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            state = states[4]
            start_time = time.time()
        elif (msg == "i'm good" or msg == "i'm fine") and state == states[4]:
            state = states[9]
            start_time = time.time()
        elif (msg == 'how about you?' or msg == 'and yourself?') and state == states[9]:
            speech_choice = random.choice(
                ["I’m good", "I'm fine, thanks for asking"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            state = states[5]
            start_time = time.time()
        elif msg == 'dev-join':
            # Add 5 for the approximate time for server latency/ actualy bot joining speeds.
            start_time = time.time() + 5
        # bot-commands
        # If hi or hello occurs and its not in any of the states make it its own command
        elif (msg == 'hi' or msg == 'hello'):
            irc.send(channel, f"{sender}: Wazzaaaaaaap")
        elif msg == 'die':
            irc.send(channel, f"{sender}: really? OK, fine.")
            irc.command("QUIT")
            sys.exit()
        elif msg == 'forget':
            irc.send(
                channel, f"{sender}: forgetting everything")
            start_time = time.time()
            state = states[0]
        elif msg == 'who are you?' or msg == 'usage':
            irc.send(
                channel, f"{sender}: My name is {botnick}. I was created by Luke Rowe, Brandon Kwe, Yaniv Sagy, and Jeremiah Lee, CSC 482-03")
            irc.send(
                channel, f"{sender}: Luke's Q/A can be used by asking a question with `who` and `president` along with `a number` that can be both numerical or ordinal, i.e. first, second, third.")
            irc.send(
                channel, f"{sender}: It can also be queried by saying `tell me more about ` and a presidents name you want, it can be impercise.")
            irc.send(
                channel, f"{sender}: Brandon's Q/A can also answer questions about birthdays. Just ask: 'When was [name] born?")
            irc.send(
                channel, f"{sender}: Yaniv's Q/A can also answer questions about NBA game outcomes between the 2015 season to the 2022 season.")
            irc.send(channel, f"{sender}: Just ask questions along the lines of: `NBA: Who [beat/won against/defeated/lost to/lost against/fell to] [NBA team] on [date]?`, `NBA: Who did [NBA team] [beat/win against/defeat/lose to/fall to] on [date]?`, `NBA: Who did [NBA team] play against on [date]?`, or `NBA: Who played against [NBA team] on [date]?` The dates can be entered in one of the following forms: `MM/DD/YYYY`, `MM/YYYY`, or `YYYY`.")
            irc.send(
                channel, f"{sender}: Jeremiah's Q/A can translate text. As an example, you can say \"Translate this into German: Good Morning\". It also supports alternate prompt forms such as \"Translate this ...\" or \"Translate this French into Swedish: ...\" etc")
        elif msg == 'users':
            users = user_list(irc)
            irc.send(channel, f"{sender}: {users}")
        elif msg != 'dev-pass' and state == 'START':
            phase_3(irc, msg, sender)


def phase_3(irc, msg, sender, channel=channel):
    """
    Phase 3 implements, allow each member to run code individually and creates a dedicated module area to do so.
    """ 
    luke_bot.luke_bot(irc, msg, sender, channel)
    brandon_bot.brandon_bot(irc, msg, sender, channel)
    yaniv_bot.yaniv_bot(irc, msg, sender, channel)
    jeremiah_bot.jeremiah_bot(irc, msg, sender, channel)


def response_filter(text: str):
    """
    Break a given response into components.
    Return either the sanitized text components or a 4-tuple None for naughty inputs.
    """
    text_p = []  # sender, type, target, message
    # everything after 3 is a part of the message

    if f':{botnick} MODE {botnick} :+iw' in text:
        text = f':Guest35!~Guest35@2600:8800:15:3700::18a4 PRIVMSG {channel} :{botnick}: dev-join'
    for t in text.split(maxsplit=3):
        text_p.append(t)

    if len(text_p) != 4:  # if the split got anything less than 4 ignore it
        return None, None, None, None
    if text_p[1] != 'PRIVMSG':
        return None, None, None, None
    if text_p[2] != channel:
        return None, None, None, None
    if f':{botnick}: ' not in text_p[3]:  # format for mentioning botnick
        return None, None, None, None
    # split the message with !, everything else is user client data
    text_p[0] = text_p[0].split('!')[0]
    text_p[0] = text_p[0][1:]  # remove the : char at the start

    # remove ':' then its own username and ': ' from message and trailing newlines
    text_p[3] = text_p[3][len(botnick)+3:].rstrip()

    # vals to make processing easier
    return text_p[0], text_p[1], text_p[2], text_p[3].lower()


def user_list(irc: IRC):
    """
    Issue a NAME command to the channel and sanitize the response.
    Return usernames in a string.
    """
    text = ''
    while botnick not in text or 'End of /NAMES list' in text: # run until a good /NAMES cmd is returned
        irc.command(f"NAMES {channel}")
        text = irc.get_response(0) # Waiting for next response can get overrun by spam, could beat serv. resp for cmd
    text = text.split(f'{channel} :')[1]
    text = text.split(':')[0]
    text = text.split()
    output = []
    for t in text:
        output.append(t)
    print(f'USER CMD: {text}')
    return ", ".join(output)


if __name__ == "__main__":
    main()
