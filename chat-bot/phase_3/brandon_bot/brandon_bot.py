import wikipediaapi
import re

def brandon_bot(irc, msg, sender, channel):
    if re.search('when was [a-zA-Z ]+ born\?', msg):
        name = ' '.join(msg.split()[2:-1])
        print(f"NAME: {name}")
        #TODO
    
    print("Called brandon_bot()")
    return