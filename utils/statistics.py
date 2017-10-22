import threading
import discord
import asyncio
from time import gmtime, strftime, sleep
from utils import gspread_api


client = None

msgid = ""
channelid = "307085753744228356"

msgcount = 0


async def setServerStats():
    await client.wait_until_ready()
    await asyncio.sleep(3)
    while not client.is_closed:
        global msgid
        dataset = gspread_api.get_stats()
        out = {
            "All Users Peak": dataset[0],
            "Max Online Peak": dataset[1],
            "Average Online Members": dataset[3],
            "Average Online Suporters": dataset[5],
            "Average on. Membs / Supp": dataset[6],
            "Max on. Membs / Supp:": dataset[8],
            "Collected Datasets": dataset[4]
        }
        em = discord.Embed(color=discord.Color.gold(), title="SERVER STATISTICS")
        em.description = "See full stats **[here](https://s.zekro.de/dcstats)**\n\n*Last update: %s*\n*This will be updated every 10 minutes.*" % strftime("%Y-%m-%d %H:%M:%S", gmtime())
        for k, v in out.items():
            em.add_field(name=k, value=v, inline=False)
        chan = list([c for c in list(client.servers)[0].channels if c.id == channelid])[0]
        if msgid == "":
            msg = await client.send_message(chan, embed=em)
            msgid = msg.id
        else:
            await client.edit_message(await client.get_message(chan, msgid), embed=em)
        await asyncio.sleep(10 * 60)


def action():
    while not client.is_closed:
        date = strftime("%d.%m.%Y %H:%M", gmtime())
        server = list(client.servers)[0]
        users = server.members
        supprole = discord.utils.get(server.roles, name="Supporter")

        members = [u for u in users if not u.bot]
        online = [m for m in members if not str(m.status) == "offline"]
        suppsonline = [m for m in online if supprole in m.roles]

        global msgcount
        gspread_api.append([date, len(members), len(online), len(suppsonline), msgcount])
        msgcount = 0
        sleep(30 * 60)


def run():
    t = threading.Thread(target=action)
    t.start()
