import csv
import re

def luke_bot(irc, msg, sender, channel):
    if not('who' in msg and 'pres' in msg):  # who was the 42 president, also generalize, so that any form of the question will be picked up
        return
    
    pres_num = parser(msg)
    if isinstance(pres_num, str):  # if pres_num is an error msg
        irc.send(
            channel, f"{sender}: {pres_num}")
        return
    
    pres_num = int(pres_num)
    irc.send(
        channel, f"{sender}: Here is some more info about president number {pres_num}.")
    with open('stripped_pres_info.txt', 'r') as f:
        reader = csv.reader(f)
        next(reader) #skip header
        # 0        , 1        , 2         , 3         , 4        , 5         , 6            , 7
        # [pres_num, pres_name, pres_birth, pres_death, pres_term, pres_party, pres_election, pres_VP]
        for row in reader:
            if int(row[0]) == pres_num:
                out_msg =f"{row[1]} was the president #{row[0]}, they were born, {row[2]}, and "
                if int(row[3]) == -1:
                    out_msg += 'are still alive.'
                else:
                    out_msg += f'died {row[3]}.'
                irc.send(channel, f'{sender}: {out_msg}')
                out_msg = f"They served from {row[4].replace('<comma>', ',')} with {row[7].replace('|', ' and ').replace('<comma>', ',')} as their VP, their parties were {row[5].replace('|', ' and ')} respectively."
                irc.send(channel, f'{sender}: {out_msg}')
                if row[6] == '-': #i.e. pres 10
                    out_msg = f"They assumed office after the previous president died."
                elif '-' in row[6]: #i.e. pres 33
                    out_msg = f"They assumed office after the previous president died, then were re-elected in {row[6].replace('-|', '')}."
                else:
                    out_msg = f"They were elected {row[6].replace('|', ' and ')}."
                irc.send(channel, f'{sender}: {out_msg}')


def parser(msg):  # TODO: make it parse multiple ways of saying nums
    msg = re.search(r'\d+', msg).group()
    try:
        msg = int(msg)
        if msg <= 0 or msg >= 48:
            # TODO: potentially update this
            return 'Sorry but there was no president with the number {msg} yet.'
    except:
        return 'Sorry but I couldnt parse what number president you wanted.'
    return msg
