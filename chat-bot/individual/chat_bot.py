from IRC import IRC
import sys

## IRC Config
server = "irc.libera.chat" 	# Provide a valid server IP/Hostname
port = 6667
channel = "#CSC482"
botnick = "pog-bot"
botnickpass = ""		# in case you have a registered nickname 		
botpass = ""			# in case you have a registered bot	

irc = IRC()
irc.connect(server, port, channel, botnick, botpass, botnickpass)

def user_list():
    irc.command(f"NAMES {channel}") #NAMES gives back a list of users with yucky extra text
    text = irc.get_response()
    text = text.split(f'{channel} :')[1]
    text = text.split(':')[0]
    text = text.split()
    output = []
    for t in text:
        output.append(t)
    return ", ".join(output)

while True:
    text = irc.get_response()
    print("RECEIVED ==> ",text)

    text_p = [] #sender, type, target, message
    for t in text.split(maxsplit=3): # everything after 3 is apart of the message splits into 4 parts
        text_p.append(t)

    # continue if any criterium aren't met
    if len(text_p) != 4: #if the split got anything less than 4 ignore it
        continue
    if text_p[1] != 'PRIVMSG':
        continue
    if text_p[2] != '#CSC482':
        continue
    if f':{botnick}: '  not in text_p[3]: #format for mentioning botnick
        continue
    text_p[0] = text_p[0].split('!')[0] #split the message with !, everything else is user client data
    text_p[0] = text_p[0][1:] #remove the : char at the start

    text_p[3] = text_p[3][len(botnick)+3:].rstrip() # remove ':' then its own username and ': ' from message and trailing newlines

    #vals to make processing easier
    sender = text_p[0]
    m_type = text_p[1]
    m_tar = text_p[2]
    msg = text_p[3]

    print(f'accepted text: {text_p}')

    if msg == 'die':
        irc.send(channel, f"{sender}: really? OK, fine.")
        irc.command("QUIT")
        sys.exit()

    if msg == 'who are you?' or msg == 'usage':
        irc.send(channel, f"{sender}: My name is pog-bot. I was created by Luke Rowe, Brandon Kwe, Yaniv Sagy, and Jeremiah Lee, CSC 482-03")
        irc.send(channel, f"{sender}: I can answer questions about mice! Ask me a question like this: 'Can a mouse defeat a cat in battle?'") #TODO: Update when done with phase 3
        pass

    if msg == 'users':
        users = user_list()
        irc.send(channel, f"{sender}: {users}")

    if msg == 'hi' or msg == 'hello':
        irc.send(channel, f"{sender}: Wazzaaaaaaap")
