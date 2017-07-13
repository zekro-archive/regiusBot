import asyncio
import operator
from os import path, mkdir
from time import strftime, gmtime

import discord

import gspread_api

client = None

MESSAGE_XP_VAL = 5
ONLINE_XP_VAL = 50
ONLINE_TIMEOUT = 60 * 30 # (30 Minuten)


# Speichert das Dictionary {"Member ID":xp_value} als CSV in SAVES/level.csv
def save(table):

    if not path.isdir("SAVES"):
        mkdir("SAVES")

    with open("SAVES/level.csv", "w") as f:
        for key in table.keys():
            f.write(key + "," + str(table[key]) + "\n")


# Liest die SAVES/level.csv Datei und returnt die serialisierten Daten wieder
# als Dictionary {"Member ID":xp_value}
def get_table():

    file = "SAVES/level.csv"
    out = {}

    if path.isfile(file):
        with open(file) as f:
            for line in f.readlines():
                out[line.split(",")[0]] = int(line.split(",")[1])
    return out


# Diese Funktion wird alle 30 Minuten ausgeführt und fügt jedem online Member
# 10 XP hinzu und speichert das in der CSV Datei
@asyncio.coroutine
def add_time_xp():
    yield from client.wait_until_ready()
    while not client.is_closed:
        table = get_table()
        for memb in filter(lambda m: not m.bot and not m.status.__str__() == "offline", list(client.servers)[0].members):
            if table.__contains__(memb.id):
                table[memb.id] += ONLINE_XP_VAL
            else:
                table[memb.id] = ONLINE_XP_VAL
        save(table)
        yield from asyncio.sleep(ONLINE_TIMEOUT)


@asyncio.coroutine
def level_to_scoreboard():
    yield from client.wait_until_ready()
    while not client.is_closed:

        d = get_table()
        table = dict([(k, d[k]) for k in sorted(d, key=d.get, reverse=True)])
        server = list(client.servers)[0]
        outstr = ":scroll:   __**SCOREBOARD**__  :scroll: \n\n"

        for id in table:
            memb = discord.utils.get(server.members, id=id)
            if not memb == None:
                xp = table[id]
                lvl = str(int(xp / 1000))
                if len(lvl) < 2:
                    lvl = "0" + lvl
                outstr += ":white_small_square:   **[LVL %s]**    %s  -  `%s XP`\n" % (lvl, memb.name, xp)

        try:
            msg = yield from client.get_message(channel=discord.utils.get(server.channels, name="scoreboard"), id="334789295091089428")
            yield from client.edit_message(msg, outstr[0:2000])
        except:
            raise

        yield from asyncio.sleep(60)


# Fügt dem author einer versendeten Message 5 XP hinzu
def add_message_xp(author):

    table = get_table()

    if not author.bot:
        if table.__contains__(author.id):
            table[author.id] += MESSAGE_XP_VAL
        else:
            table[author.id] = MESSAGE_XP_VAL
        save(table)


def get_xp(member):
    table = get_table()
    if table.__contains__(member.id):
        return table[member.id]
    return 0


def list_xp():
    return get_table()