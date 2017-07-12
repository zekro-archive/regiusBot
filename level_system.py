import asyncio
from os import path, mkdir

client = None

MESSAGE_XP_VAL = 5
ONLINE_XP_VAL = 10
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

    table = get_table()

    while not client.is_closed:
        for memb in filter(lambda m: not m.bot and not m.status.__str__() == "offline", list(client.servers)[0].members):
            if table.__contains__(memb.id):
                table[memb.id] += ONLINE_XP_VAL
            else:
                table[memb.id] = ONLINE_XP_VAL
        save(table)
        yield from asyncio.sleep(ONLINE_TIMEOUT)


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