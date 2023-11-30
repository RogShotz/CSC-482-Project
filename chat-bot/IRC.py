import socket
import sys
import time
import threading

# PROVIDED BY DR. FOAAD CSC 482, Modified by Luke


class IRC:

    irc = socket.socket()

    def __init__(self):
        # Deefine the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = ''
        self.botnick = ''

    def command(self, msg):
        self.irc.send(bytes(msg + "\n", "UTF-8"))

    def send(self, channel, msg):
        # Transfer data
        self.command("PRIVMSG " + channel + " :" + msg)

    def connect(self, server, port, channel, botnick, botpass, botnickpass):
        self.channel = channel
        self.botnick = botnick
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.command("USER " + botnick + " " +
                     botnick + " " + botnick + " :python")
        self.command("NICK " + botnick)
        # self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))

        # join the channel
        self.command("JOIN " + channel)

    def get_response(self, timeout = 0):
        # Get the response
        if not timeout:
            resp = self.irc.recv(2040).decode("UTF-8")
            return resp
        self.irc.settimeout(timeout)
        try:
            resp = self.irc.recv(2040).decode("UTF-8")
        except:  # if timed out get special dev-pass input for bot to recognize and process as nothing
            resp = f':Guest35!~Guest35@2600:8800:15:3700::18a4 PRIVMSG {self.channel} :{self.botnick}: dev-pass'
        if resp.find('PING') != -1:
            self.command('PONG ' + resp.split()[1] + '\r')

        return resp
