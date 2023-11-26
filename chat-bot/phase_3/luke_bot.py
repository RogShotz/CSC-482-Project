def luke_bot(irc, msg, sender, channel):
    if msg == 'example':
        irc.send(
                channel, f"{sender}: example bot q/a")
        pass
    return