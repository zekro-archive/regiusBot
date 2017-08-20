import threading
import discord

from utils import gspread_api
from time import strftime, gmtime, sleep


client = None


def action():
    while not client.is_closed:
        date = strftime("%d.%m.%Y %H:%M", gmtime())
        server = list(client.servers)[0]
        users = server.members
        supprole = discord.utils.get(server.roles, name="Supporter")

        members = [u for u in users if not u.bot]
        online = [m for m in members if not str(m.status) == "offline"]
        suppsonline = [m for m in online if supprole in m.roles]

        gspread_api.append([date, len(members), len(online), len(suppsonline)])
        sleep(30 * 60)


def run():
    t = threading.Thread(target=action)
    t.start()
