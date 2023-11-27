import pandas as pd

def yaniv_bot(irc, msg, sender, channel):
    df_nba = pd.read_csv('nba_data.csv')
    print(df_nba)
    if msg == 'example':
        irc.send(
                channel, f"{sender}: example bot q/a")
        pass
    return

df_nba = pd.read_csv('nba_data.csv')
print(df_nba)