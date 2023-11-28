from IRC import IRC
import sys
import time
import random
from phase_3.luke_bot import luke_bot
from phase_3.yaniv_bot import yaniv_bot
from phase_3.brandon_bot import brandon_bot

# IRC Config
server = "irc.libera.chat" 	# Provide a valid server IP/Hostname
port = 6667
channel = "#CSC482"
botnick = "pog-bot"
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
        text = irc.get_response()
        sender, m_type, m_tar, msg = response_filter(text)
        # Timer must go before rejection so that it is being updated per timeout as well.
        if msg == 'dev-pass':
            print(f'passed: {state}')
        if time.time() - start_time >= 15:
            if state == 'START':  # For targetting a person for conversation.
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
                state = 'START' # reset
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
            speech_choice = random.choice(['how are you?', "what's happening?"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            state = states[4]
            start_time = time.time()
        elif (msg == "i'm good" or msg == "i'm fine") and state == states[4]:
            state = states[9]
            start_time = time.time()
        elif (msg == 'how about you?' or msg == 'and yourself?') and state == states[9]:
            speech_choice = random.choice(["I’m good", "I'm fine, thanks for asking"])
            irc.send(channel, f"{convo_target}: {speech_choice}")
            state = states[5]
            start_time = time.time()
        elif msg == 'dev-join':
            start_time = time.time() + 5 # Add 5 for the approximate time for server latency/ actualy bot joining speeds.
        # bot-commands
        elif (msg == 'hi' or msg == 'hello'): # If hi or hello occurs and its not in any of the states make it its own command
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
            # TODO: Update when done with phase 3
            irc.send(
                channel, f"{sender}: I can answer questions about mice! Ask me a question like this: 'Can a mouse defeat a cat in battle?'")
        elif msg == 'users':
            users = user_list(irc)
            irc.send(channel, f"{sender}: {users}")
        elif msg != 'dev-pass':
            phase_3(irc, msg, sender)


def phase_3(irc, msg, sender, channel=channel):
    """
    Phase 3 implements, allow each member to run code individually and creates a dedicated module area to do so.
    """
    luke_bot.luke_bot(irc, msg, sender, channel)
    brandon_bot.brandon_bot(irc, msg, sender, channel)
    #yaniv_bot.yaniv_bot(irc, msg, sender, channel)


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
    irc.command(f"NAMES {channel}")
    text = irc.get_response()
    text = text.split(f'{channel} :')[1]
    text = text.split(':')[0]
    text = text.split()
    output = []
    for t in text:
        output.append(t)
    return ", ".join(output)


if __name__ == "__main__":
    main()
