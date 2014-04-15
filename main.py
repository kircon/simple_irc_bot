import bot
import time

t = bot.MyBot()
t.start()
inputs = []
while 1:
    inputs = t.getinputs()
    if len(inputs) > 0:
        print(inputs)
    time.sleep(5)

