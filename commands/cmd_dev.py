from urllib.request import urlopen

import discord

import STATICS

description = "Add roles wich languages you write in."

ignore_roles = ()

roles = []


def get_roles():
    return urlopen("https://pastebin.com/raw/7UE5euBg").read().__str__()[2:-1].split(", ")


help = "**USAGE:**\n" \
       "`!dev <lang1> <lang2> ...`\n\n" \
       "Available languages: `%s`" \
       "\n\n*If there are other languages you want to add, please contact the server owner or admin to add the role manually.*" % get_roles().__str__()[1:-1].replace("'", "")



def ex(message, client):

    for s in get_roles():
        roles.append(s)
    args = message.content.replace(STATICS.PREFIX + "dev", "")[1:].split(" ")
    roles_to_add = []
    added_roles = []
    failed_roles = []

    for s in args:
        appended = False
        if args[0] == "":
            yield from client.send_message(message.channel, embed=discord.Embed(description=help, colour=discord.Color.red()))
            return
        if not roles.__contains__(s):
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=("`%s` is not a valid language role.\n"
                                                                                                                         "Available roles: `%s`"
                                                                                                                         "\n\n*If there are other languages you want to add, please contact the server owner or admin to add the role manually.*" % (s, roles.__str__()[1:-1].replace("'", "")))))
            return
        for r in message.server.roles:
            if r.name.lower() == s:
                roles_to_add.append(r)
                added_roles.append(r.name)
                appended = True
        if not appended:
            failed_roles.append(s)

    for r in roles_to_add:
        yield from client.add_roles(message.author, r)

    if len(failed_roles) == 0:
        failed_roles.append("none")
    yield from client.send_message(message.channel, embed=discord.Embed(description=("Added roles\n"
                                                                                     "`%s`\n\n"
                                                                                     "Failed to add roles\n"
                                                                                     "`%s`\n\n"
                                                                                     "*If there are other languages you want to add, please contact the server owner or admin to add the role manually.*") % (added_roles.__str__()[1:len(added_roles.__str__())-1].replace("'", ""), failed_roles.__str__()[1:len(failed_roles.__str__())-1].replace("'", ""))))