import csv
import re

num_conv = {'first': 1,
            'second': 2,
            'third': 3,
            'fourth': 3,
            'fifth': 3,
            'sixth': 3,
            'seventh': 3,
            'eighth': 3,
            'nineth': 3,
            'tenth': 3,
            'eleventh': 3,
            'twelveth': 3,
            }
num_prefix = {'twenty': 20,
              'thirty': 30,
              'forty': 40,
              'fifty': 50,
              'sixty': 60,
              'seventy': 70,
              'eighty': 80,
              'ninety': 90}


def luke_bot(irc, msg, sender, channel):
    """
    Handle messages that contain 'who and pres' or 'tell me more about {president name}' and respond to it.
    """
    if not (('who' in msg and 'pres' in msg) or ('tell me more about ' in msg)):
        return
    if 'who' in msg and 'pres' in msg:
        pres_num = parser(msg)
        if isinstance(pres_num, str):  # if pres_num is an error msg
            irc.send(
                channel, f"{sender}: {pres_num}")
            return

        pres_num = int(pres_num)
    else:
        msg = msg.replace('tell me more about ', '').lower()
        if len(msg) < 4:  # stops short inputs from getting in and spamming presidents
            irc.send(
                channel, f"{sender}: sorry but {msg} is too short a name for me to search for.")
            return
        pres_num = -1
    with open('./phase_3/luke_bot/stripped_pres_info.txt', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        # 0        , 1        , 2         , 3         , 4        , 5         , 6            , 7
        # [pres_num, pres_name, pres_birth, pres_death, pres_term, pres_party, pres_election, pres_VP]
        for row in reader:
            if int(row[0]) == pres_num or msg in row[1].lower():
                # Response formatting and editing from CSV
                irc.send(
                    channel, f"{sender}: Here is some more info about president number {row[0]}.")
                out_msg = f"{row[1]} was president #{row[0]}. They were born, {row[2]}, and "
                if int(row[3]) == -1:
                    out_msg += 'are still alive.'
                else:
                    out_msg += f'died in {row[3]}.'
                irc.send(channel, f'{sender}: {out_msg}')
                out_msg = f"They served from {row[4].replace('<comma>', ',')} with {row[7].replace('|', ' and ').replace('<comma>', ',')} as their VP, their parties were {row[5].replace('|', ' and ')} respectively."
                irc.send(channel, f'{sender}: {out_msg}')
                if row[6] == '-':  # i.e. pres 10
                    out_msg = f"They assumed office after the previous president died."
                elif '-' in row[6]:  # i.e. pres 33
                    out_msg = f"They assumed office after the previous president died, then were re-elected in {row[6].replace('-|', '')}."
                else:
                    out_msg = f"They were elected {row[6].replace('|', ' and ')}."
                irc.send(channel, f'{sender}: {out_msg}')


def parser(msg):
    """
    Parse the message to look for numbers to return.
    Return: the number or an error message
    """
    msg_search = re.search(r'\d+', msg)
    if msg_search:
        msg = msg_search.group()
    else:
        msg_split = msg.split(' ')
        num = 0
        for m in msg_split:
            for prefix in num_prefix.keys():
                if prefix in m:
                    num += num_prefix.get(prefix)
            for num_amt in num_conv.keys():
                if num_amt in m:
                    num += num_conv.get(num_amt)
        msg = num
    try:
        msg = int(msg)
        if msg <= 0 or msg >= 48:
            return f'Sorry but there was no president with the number {msg} yet.'
    except:
        return 'Sorry but I couldnt parse what number president you wanted.'
    return msg
