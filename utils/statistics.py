import threading

from utils import gspread_api
from time import strftime, gmtime, sleep


client = None


def action():
    while not client.is_closed:
        date = strftime("%d.%m.%Y %H:%M", gmtime())
        members = len(list(filter(lambda m: not m.bot, list(client.servers)[0].members)))
        online = len(list(filter(lambda m: m.status.__str__() != "offline" and (not m.bot), list(client.servers)[0].members)))
        gspread_api.append([date, members, online])
        sleep(30 * 60)


def run():
    t = threading.Thread(target=action)
    t.start()
