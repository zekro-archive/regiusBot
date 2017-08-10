from discord import Embed, Color
from utils import level_system, userbots
from commands import cmd_github


description = "Get information about user."


CLIENT = None
CHANNEL = None
SERVER = None
AUTHOR = None


async def ex(message, client):

    global CLIENT, CHANNEL, SERVER
    CLIENT = client
    CHANNEL = message.channel
    SERVER = message.server
    args = message.content.split()[1:]

    try:
        mentions = message.mentions
        if len(mentions) > 0:
            user = mentions[0]
        elif len(args) > 0:
            david_getter = [m for m in SERVER.members if m.id == args[0]]
            if len(david_getter) > 0:
                user = david_getter[0]
            else:
                raise Exception
        else:
            raise Exception
    except:
        await client.send_message(CHANNEL, embed=Embed(color=Color.red(), description="Please enter a valid user ID or mention!"))
        return


    def _format_time(t):
        def _beautify(inp):
            return "0" + str(inp) if inp < 10 else str(inp)
        return "%s.%s.%s - %s:%s:%s" \
               % (_beautify(t.day), _beautify(t.month), t.year, _beautify(t.hour), _beautify(t.minute), _beautify(t.second))

    def _get_xp():
        xp = level_system.get_xp(user)
        level = int(int(xp) / 1000)
        progress = (int(xp) % 1000) / 1000
        progress_bar = "[" + "===================="[:int(progress * 20)] + "                    "[int(progress * 20):] + "]\n\n   " + str(int(progress * 100)) + "% to next LVL"
        return "**LVL `%s`** (%s XP)\n```%s```" % (level, xp, progress_bar)

    def _get_github():
        cmd_github.SERVER = message.server
        current = cmd_github.get_list()
        return ":link:   **[%s](%s)**" % (current[user], current[user]) if user in current else "No GitHub profile linked."

    def _get_bots():
        out = []
        bots = userbots.get_botlist(SERVER)
        count = 0
        for u in [u for u in bots.values() if u == user]:
            out.append([k.mention for k, v in bots.items() if v == u][count])
            count += 1
        return out


    data = {
        "Name": user.name,
        "Nickname": user.name,
        "ID": user.id,
        "Tag": user.name + "#" + user.discriminator,
        "Roles": ", ".join([r.name for r in user.roles]),
        "Joined server": _format_time(user.joined_at),
        "Joined Discord": _format_time(user.created_at),
        "GitHub:": _get_github(),
        "Bots:": " ".join(_get_bots()) if len(_get_bots()) > 0 else "No bots on this guild",
        "XP / Level": _get_xp(),
    }

    em = Embed(description="**__" + data["Name"] + "'s user profile__**\n\n", color=Color.gold())
    if user.avatar_url is not None:
        em.set_thumbnail(url=user.avatar_url)
    for k, v in data.items():
        em.add_field(name=k, value=v, inline=False)

    await client.send_message(CHANNEL, embed=em)
