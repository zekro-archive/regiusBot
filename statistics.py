import threading
from time import sleep, strftime, gmtime

from os import path, mkdir

server = None


def action():

    date = strftime("%d.%m.%Y %H:%M", gmtime())
    members = len(list(filter(lambda m: not m.bot, server.members)))
    online = len(list(filter(lambda m: m.status.__str__() != "offline" and (not m.bot), server.members)))
    out = "%s,%s,%s\n" % (date, members, online)

    with open("SAVES/statistics.csv", "a") as f:
        f.write(out)

    sleep(60*10)
    action()


def start():

    p = "SAVES"
    if not path.isdir(p):
        mkdir(p)

    t = threading.Thread(target=action)
    t.start()
