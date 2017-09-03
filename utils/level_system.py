import asyncio
from os import path, mkdir
from utils import gspread_api

import discord

client = None

MESSAGE_XP_VAL = 5
ONLINE_XP_VAL = 5
ONLINE_TIMEOUT = 60 * 30  # (30 Minuten)


# Speichert das Dictionary {"Member ID":xp_value} als CSV in SAVES/level.csv
def save(table):

    g = gspread_api.Settings("dd_saves", 0)
    g.set_dict(table)


# Liest die SAVES/level.csv Datei und returnt die serialisierten Daten wieder
# als Dictionary {"Member ID":xp_value}
def get_table():

    g = gspread_api.Settings("dd_saves", 0)
    temp = g.get_dict()
    return dict([(k, int(v)) for k, v in temp.items()])



# Diese Funktion wird alle 30 Minuten ausgeführt und fügt jedem online Member
# 10 XP hinzu und speichert das in der CSV Datei
async def add_time_xp():
    await client.wait_until_ready()
    while not client.is_closed:
        table = get_table()
        for memb in filter(lambda m: not m.bot and not m.status.__str__() == "offline", list(client.servers)[0].members):
            if table.__contains__(memb.id):
                table[memb.id] += ONLINE_XP_VAL
            else:
                table[memb.id] = ONLINE_XP_VAL
        save(table)
        await asyncio.sleep(ONLINE_TIMEOUT)


async def level_to_scoreboard():
    await client.wait_until_ready()

    while not client.is_closed:

        d = get_table()
        table = dict([(k, d[k]) for k in sorted(d, key=d.get, reverse=True)])
        server = list(client.servers)[0]

        outstr = ":scroll:   __**SCOREBOARD**__ (Top 20)  :scroll: \n\n"

        _count = 0
        for id in table:
            memb = discord.utils.get(server.members, id=id)
            if memb is not None:
                _count += 1
                xp = table[id]
                lvl = str(int(xp / 1000))
                if len(lvl) < 2:
                    lvl = "0" + lvl
                outstr += "%s.  -  **[LVL %s]**    %s  -  `%s XP`\n" % (_count, lvl, memb.name, xp)
                if _count >= 20:
                    break

        try:

            msg = await client.get_message(channel=discord.utils.get(server.channels, name="scoreboard"), id="334789295091089428")
            await client.edit_message(msg, outstr[:2000])
        except:
            raise

        await asyncio.sleep(60)


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
