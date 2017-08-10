from discord import Embed, Color, utils
from os import path, mkdir


description = "Link your github account."

help = "**USAGE:**\n" \
       ":white_small_square:  `!github add <username/pofile link>`\n" \
       ":white_small_square:  `!github change <username/pofile link>`\n" \
       ":white_small_square:  `!github remove`\n" \
       ":white_small_square:  `!github list`\n" \
       ":white_small_square:  `!github <@mention>`\n"

savefile = "SAVES/gitlinks.dat"

CLIENT = None
CHANNEL = None
SERVER = None
AUTHOR = None


async def error(content):
    return await CLIENT.send_message(CHANNEL, embed=Embed(color=Color.red(), description=content))


async def message(content, clr=Color.default()):
    return await CLIENT.send_message(CHANNEL, embed=Embed(color=clr, description=content))


def check_path():
    if not path.isdir("SAVES"):
        mkdir("SAVES")


def get_member(membid):
    return utils.get(SERVER.members, id=membid)


def get_list():
    check_path()
    if not path.isfile(savefile):
        return {}
    out = {}
    with open(savefile) as f:
        for line in f.readlines():
            memb = get_member(line.split(":::")[0])
            if memb is not None:
                out[memb] = line.split(":::")[1].replace("\n", "")
    return out


def save_list(indict):
    check_path()
    with open(savefile, "w") as f:
        for k, v in indict.items():
            f.write("%s:::%s\n" % (k.id, v))


async def add(args):
    current = get_list()
    gitlink = args[0] if "https://github.com" in args[0] \
                         or "http://github.com" in args[0] \
                         or "www.github.com" in args[0] \
                         else "http://github.com/" + args[0]
    if AUTHOR in current.keys():
        await error("You are already registered in the list!\nUse `!github change` to change your entry.")
    else:
        current[AUTHOR] = gitlink
        save_list(current)
        await message("Successfully assigned [%s](%s) to member %s." % (gitlink, gitlink, AUTHOR.mention), Color.green())


async def edit(args):
    current = get_list()
    gitlink = args[0] if "https://github.com" in args[0] \
                         or "http://github.com" in args[0] \
                         or "www.github.com" in args[0] \
                         else "http://github.com/" + args[0]
    if AUTHOR not in current.keys():
        await error("You are currently not registered in this list!\nUse `!github add` to add an entry.")
    elif gitlink in current.values():
        await error("The same link is still registered in the list!")
    else:
        current[AUTHOR] = gitlink
        save_list(current)
        await message("Successfully assigned [%s](%s) to member %s." % (gitlink, gitlink, AUTHOR.mention), Color.green())


async def send_list():
    current = get_list()
    out = "\n".join([":white_small_square:   [%s](%s)" % (k.name if k.nick is None else k.nick, v) for k, v in current.items()])
    await CLIENT.send_message(CHANNEL, embed=Embed(title="GitHub Profiles",
                                                   color=Color.blue(),
                                                   description=out))


async def remove_entry():
    current = get_list()
    if AUTHOR not in current.keys():
        await error("You are not registered in this list, so why to remove you form it? :^)")
    else:
        del current[AUTHOR]
        save_list(current)
        await message("Successfully removed you from the list.", Color.orange())


async def get(user):
    current = get_list()
    if user not in current.keys():
        await error("User %s is currently not registered in this list!" % user.mention)
    else:
        await message("**[%s](%s)**" % (user.name if user.nick is None else user.nick, current[user]))


async def ex(message, client):
    global CLIENT, CHANNEL, SERVER, AUTHOR
    CLIENT = client
    SERVER = message.server
    CHANNEL = message.channel
    AUTHOR = message.author

    args = message.content.split()[1:]
    mentions = message.mentions

    if len(mentions) > 0:
        await get(mentions[0])
    elif len(args) > 1:
        if args[0] == "add":
            await add(args[1:])
        elif args[0] == "change" or args[0] == "edit":
            await edit(args[1:])
    elif len(args) > 0:
        if args[0] == "list":
            await send_list()
        elif args[0] == "remove" or args[0] == "delete":
            await remove_entry()
