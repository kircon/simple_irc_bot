import socket
import threading


class MyBot(threading.Thread):

    host = ""
    port = 0
    s = socket.socket()

    nick = ""
    ident = ""
    master = ""
    channel = ""
    quit = False
    inputs = []
    inputs_read = False

    # Respond to pings
    def ping(self):
        self.s.send(bytes("PONG :Pong\n", 'UTF-8'))

    # Send messages to channel.
    def sendmsg(self, chan, msg):
        self.s.send(bytes("PRIVMSG " + chan + " :" + msg + "\n", 'UTF-8'))

    # Join channels
    def joinchan(self, chan):
        self.s.send(bytes("JOIN " + chan + "\n", 'UTF-8'))

    # This function responds to a user that inputs "Hello Botname"
    def hello(self, newnick):
        self.s.send(bytes("PRIVMSG " + self.channel + " :Hello " + newnick + "!\n", 'UTF-8'))

    # Possible commands for the bot in format "Botname: command"
    def commands(self, name, chan, message):
        if message.find(self.nick + ': is what?') != -1:
            self.s.send(bytes('PRIVMSG %s :%s: I is awesome!\r\n' % (chan, name), 'UTF-8'))
        elif message.find(self.nick + ': help') != -1:
            self.s.send(bytes('PRIVMSG %s :%s: My other command is what?.\r\n' % (chan, name), 'UTF-8'))

    # Looking for inputs in message and delete list if it was already read
    def findinput(self, msg):
        if msg.find(":up") != -1:
            self.inputs.append("up")
        elif msg.find(":down") != -1:
            self.inputs.append("down")
        elif msg.find(":left") != -1:
            self.inputs.append("left")
        elif msg.find(":right") != -1:
            self.inputs.append("right")

    # Poll inputs
    def getinputs(self):
        self.inputs_read = True
        return self.inputs

    # initialize settings and connect to channel
    def __init__(self, host="chat.freenode.net", port=6667, channel="#mytestchannel", nick="Blorgbot",
                 ident="Blablubb", master="Blorg"):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.channel = channel
        self.nick = nick
        self.ident = ident
        self.master = master

        self.s.connect((self.host, self.port))

        self.s.send(bytes("NICK %s\r\n" % self.nick, "UTF-8"))
        self.s.send(bytes("USER %s %s bla :%s\r\n" % (self.ident, self.host, "nope"), "UTF-8"))
        self.joinchan(self.channel)

    # commence listening
    def run(self):

        self.sendmsg(self.channel, "Hello everyone!")
        while self.quit is False:

            ircmsg = self.s.recv(2048).decode("UTF-8")
            ircmsg = str(ircmsg)
            ircmsg = ircmsg.strip('\r\n')

            print(ircmsg)

            if ircmsg.find(' PRIVMSG ') != -1:
                nick = ircmsg.split('!')[0][1:]
                channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
                self.commands(nick, channel, ircmsg)

            # respond to ping
            if ircmsg.find("PING :") != -1:
                self.ping()

            # Be polite and greet back
            if ircmsg.find(":Hello " + self.nick) != -1:
                nick = ircmsg.split('!')[0][1:]
                self.hello(nick)

            self.findinput(ircmsg)
