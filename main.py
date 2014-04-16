import bot

t = bot.MyBot()
t.start()
inputs = []
while 1:
    inputs = t.getinputs()
    if len(inputs) > 0:
        print(inputs)

    # Should be done in the bot itself
    t.inputs.clear()

