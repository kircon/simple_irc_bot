import socket
import threading


class MyBot(threading.Thread):

    host = "chat.freenode.net"
    port = 6667
    s = socket.socket()

    nick = "Blorgbot"
    ident = "Blablubb"
    master = "Blorgh"
    channel = "#mytestchannel"
    quit = False
    inputs = []
    inputs_read = False

    # This is our first function! It will respond to server Pings.
    def ping(self):
        self.s.send(bytes("PONG :Pong\n", 'UTF-8'))

    # This is the send message function, it simply sends messages to the channel.
    def sendmsg(self, chan, msg):
        self.send(bytes("PRIVMSG " + chan + " :" + msg + "\n", 'UTF-8'))

    # This function is used to join channels.
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
        if self.inputs_read:
            self.inputs.clear()

        if msg.find(":up") != -1:
            self.inputs.append("up")
        elif msg.find(":down") != -1:
            self.inputs.append("down")
        elif msg.find(":left") != -1:
            self.inputs.append("left")
        elif msg.find(":right") != -1:
            self.inputs.append("right")

        self.inputs_read = False

    # Poll inputs
    def getinputs(self):
        self.inputs_read = True
        return self.inputs

    def __init__(self, host="chat.freenode.net", port=6667, channel="#mytestchannel", nick="Blorgbot",
                 ident="Blablubb", master="Blorg"):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.channel = channel
        self.nick = nick
        self.ident = ident
        self.master = master

        print("auf gehts")
        self.s.connect((self.host, self.port))

        self.s.send(bytes("NICK %s\r\n" % self.nick, "UTF-8"))
        self.s.send(bytes("USER %s %s bla :%s\r\n" % (self.ident, self.host, "nope"), "UTF-8"))
        self.joinchan(self.channel)

    def run(self):

        while self.quit is False:
            ircmsg = self.s.recv(2048).decode("UTF-8")
            ircmsg = str(ircmsg)
            ircmsg = ircmsg.strip('\r\n')

            print(ircmsg)

            if ircmsg.find(' PRIVMSG ') != -1:
                nick = ircmsg.split('!')[0][1:]
                channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
                self.commands(nick, channel, ircmsg)

            # if the server pings us then we've got to respond!
            if ircmsg.find("PING :") != -1:
                self.ping()

            # If we can find "Hello Mybot" it will call the function hello()
            if ircmsg.find(":Hello " + self.nick) != -1:
                nick = ircmsg.split('!')[0][1:]
                self.hello(nick)

            self.findinput(ircmsg)
