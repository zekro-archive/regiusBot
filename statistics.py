import threading
import gspread_api
from time import sleep, strftime, gmtime

server = None


def action():

    date = strftime("%d.%m.%Y %H:%M", gmtime())
    members = len(list(filter(lambda m: not m.bot, server.members)))
    online = len(list(filter(lambda m: m.status.__str__() != "offline" and (not m.bot), server.members)))

    gspread_api.append([date, members, online])

    sleep(10 * 60)
    action()


def start():
    t = threading.Thread(target=action)
    t.start()
