from discord import Embed, Color, utils
from os import path, mkdir
from utils import gspread_api


description = "Register bot prefixes running in this server"

help = "**USAGE:**\n" \
       ":white_small_square:  `!prefix list`\n" \
       ":white_small_square:  `!prefix add <ID of bot> <prefix>`\n" \
       ":white_small_square:  `!prefix edit <ID of bot> <new prefix>`\n" \
       ":white_small_square:  `!prefix remove <ID of bot>`\n"


savefile = "SAVES/prefixes.txt"
CLIENT = None
CHANNEL = None
SERVER = None


async def error(content):
    return await CLIENT.send_message(CHANNEL, embed=Embed(color=Color.red(), description=content))


async def message(content, clr=Color.default()):
    return await CLIENT.send_message(CHANNEL, embed=Embed(color=clr, description=content))


def check_path():
    if not path.isdir("SAVES"):
        mkdir("SAVES")


def get_bot(botid):
    try:
        return utils.get(SERVER.members, id=botid)
    except:
        return None


def get_saves():
    g = gspread_api.Settings("dd_saves", 2)
    temp = g.get_dict()
    out = {}
    for k, v in temp.items():
        bot = get_bot(k)
        if bot is not None:
            out[bot] = v
    return out


def save(indict):
    g = gspread_api.Settings("dd_saves", 2)
    g.set_dict(
        dict([(k.id, v) for k, v in indict.items()])
    )


async def add(args):
    fetching = await message("Checking data...")
    current = get_saves()
    bot = get_bot(args[0])
    pre = args[1]
    if pre.startswith("=") or pre.startswith("+"):
        await error("Please dont use a prefix staring with `=` or `+`!\n\n*This is because the bots database is running in an Google Spreadsheet wich will interpret it as function.*")
    elif bot is None:
        await error("The bot with this ID is not registered on in this server!")
    elif bot in current.keys():
        await error("The bot %s is still registered!\nUse `!prefix edit <ID of bot> <new prefix>` to edit bots prefix!" % bot.mention)
    elif pre in current.values():
        await error("The prefix ```%s``` is still used from another bot!" % pre)
    else:
        current[bot] = pre
        save(current)
        await message("Successfully registered bot %s with prefix: ```%s```" % (bot.mention, pre), Color.green())
    await CLIENT.delete_message(fetching)


async def edit(args):
    fetching = await message("Checking data...")

    current = get_saves()
    bot = get_bot(args[0])
    pre = args[1]

    if pre.startswith("=") or pre.startswith("+"):
        await error("Please dont use a prefix staring with `=` or `+`!\n\n*This is because the bots database is running in an Google Spreadsheet wich will interpret it as function.*")
    elif bot is None:
        await error("The bot with this ID is not registered on in this server!")
    elif bot not in current.keys():
        await error("The bot is not registered in this list!\nUse `!prefix add <ID of bot> <prefix>` to add your bot to the list.")
    elif pre in current.values():
        await error("The prefix ```%s``` is still used from another bot!" % pre)
    else:
        current[bot] = pre
        save(current)
        await message("Successfully set %s's prefix to ```%s```" % (bot.mention, pre), Color.green())
    await CLIENT.delete_message(fetching)


async def list_all():
    fetching = await message("Loading data...")
    current = get_saves()

    def _beautify(string):
        string = string.replace("??", "").replace("??", "")
        maxlen = max([len(k.name if k.nick is None else k.nick) for k in current.keys()])
        split = string.split("  -  ")
        beautifyedleft = split[0]
        while len(beautifyedleft) < maxlen - 1:
            beautifyedleft += " "
        return beautifyedleft + "  -  " + split[1]

    out = "```\n" \
          "%s" \
          "```" % "\n".join([_beautify("%s  -  < %s >" % (k.name if k.nick is None else k.nick, v)) for k, v in current.items()])
    await CLIENT.send_message(CHANNEL, embed=Embed(title="PREFIX LIST", description=out))
    await CLIENT.delete_message(fetching)


async def removebot(args):
    fetching = await message("Checking data...")
    current = get_saves()
    bot = get_bot(args[0])

    if bot is None:
        await error("The bot with this ID is not registered on in this server!")
    elif bot not in current.keys():
        await error("The bot is not registered in this list!\nUse `!prefix add <ID of bot> <prefix>` to add your bot to the list.")
    else:
        del current[bot]
        save(current)
        await message("Bot successfully deleted from list.")
    await CLIENT.delete_message(fetching)


async def ex(message, client):
    global CLIENT, SERVER, CHANNEL
    CLIENT = client
    SERVER = message.server
    CHANNEL = message.channel

    args = message.content.split()[1:]

    if len(args) < 1:
        await error(help)
        return

    if len(args) > 2:
        if args[0] == "add":
            await add(args[1:])
        elif args[0] == "edit":
            await edit(args[1:])
        else:
            await error(help)
    elif len(args) > 1:
        if args[0] == "remove":
            await removebot(args[1:])
        else:
            await error(help)
    else:
        if args[0] == "list":
            await list_all()
        else:
            await error(help)