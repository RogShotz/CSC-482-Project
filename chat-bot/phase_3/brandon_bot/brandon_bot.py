import wikipediaapi
import re

wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

def brandon_bot(irc, msg, sender, channel):
    if re.search('when was [a-zA-Z ]+ born\?', msg):
        name = ' '.join(msg.split()[2:-1])
        
        page_py = wiki_wiki.page(name)
        summary = page_py.summary

        start = summary.find('(')
        end = summary.find(')')
        birthday = summary[start+1:end]
        idx = birthday.find("born")
        if idx >= 0:
            irc.send(channel, birthday[idx+5:])
            return
        
        idx = birthday.find(" – ")
        if idx >=0:
            n = idx
            while n > 0 and birthday[n] != ';':
                n -= 1
            if n > 0:
                n += 2
            irc.send(channel, birthday[n:idx])
            return
            
        irc.send(channel, f"I'm sorry, I'm not sure when {name} was born.")
        return