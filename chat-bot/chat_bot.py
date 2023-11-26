from IRC import IRC
import sys
import time

# IRC Config
server = "irc.libera.chat" 	# Provide a valid server IP/Hostname
port = 6667
channel = "#CSC482"
botnick = "pog-bot"
botnickpass = ""		# in case you have a registered nickname
botpass = ""			# in case you have a registered bot


def main():
    irc = IRC()
    irc.connect(server, port, channel, botnick, botpass, botnickpass)
    start_time = time.time()
    while True:
        print('waiting...', end='')
        text = irc.get_response()
        # print("RECEIVED ==> ", text)
        sender, m_type, m_tar, msg = response_filter(text)
        if not sender:  # If the result of response_filter gives None it was no good.
            print('rejected')
            continue
        if msg != 'dev-pass':
            print(f'accepted: {msg}')

        # dev messages for internal passing, then general chat messages
        if msg == 'dev-pass':
            print('passed')
            if time.time() - start_time >= 15:
                irc.send(channel, f"{sender}: TIMER UP")
            # special dev-pass case, used to not block socket for responses
            start_time = time.time()
        elif msg == 'dev-join':
            # add 5 for the approximate time for server latency/ actualy bot joining speeds
            start_time = time.time() + 5
        elif msg == 'die':
            irc.send(channel, f"{sender}: really? OK, fine.")
            irc.command("QUIT")
            sys.exit()
        elif msg == 'forget':
            irc.send(
                channel, f"{sender}: forgetting everything")
            start_time = time.time()
            continue
        elif msg == 'who are you?' or msg == 'usage':
            irc.send(
                channel, f"{sender}: My name is pog-bot. I was created by Luke Rowe, Brandon Kwe, Yaniv Sagy, and Jeremiah Lee, CSC 482-03")
            # TODO: Update when done with phase 3
            irc.send(
                channel, f"{sender}: I can answer questions about mice! Ask me a question like this: 'Can a mouse defeat a cat in battle?'")
        elif msg == 'users':
            users = user_list(irc)
            irc.send(channel, f"{sender}: {users}")
        elif msg == 'hi' or msg == 'hello':
            irc.send(channel, f"{sender}: Wazzaaaaaaap")


def response_filter(text: str):
    """
    Break a given text into components and
    return either the sanitized text components or a 4-tuple None for naughty inputs.
    """
    text_p = []  # sender, type, target, message
    # everything after 3 is a part of the message

    if ':pog-bot MODE pog-bot :+iw' in text:
        text = ':Guest35!~Guest35@2600:8800:15:3700::18a4 PRIVMSG #CSC482 :pog-bot: dev-join'
    for t in text.split(maxsplit=3):
        text_p.append(t)

    if len(text_p) != 4:  # if the split got anything less than 4 ignore it
        return None, None, None, None
    if text_p[1] != 'PRIVMSG':
        return None, None, None, None
    if text_p[2] != '#CSC482':
        return None, None, None, None
    if f':{botnick}: ' not in text_p[3]:  # format for mentioning botnick
        return None, None, None, None
    # split the message with !, everything else is user client data
    text_p[0] = text_p[0].split('!')[0]
    text_p[0] = text_p[0][1:]  # remove the : char at the start

    # remove ':' then its own username and ': ' from message and trailing newlines
    text_p[3] = text_p[3][len(botnick)+3:].rstrip()

    # vals to make processing easier
    return text_p[0], text_p[1], text_p[2], text_p[3]


def user_list(irc: IRC):
    """Issue a NAME command and return usernames in a string."""
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
