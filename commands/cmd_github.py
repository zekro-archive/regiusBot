import discord
from os import path, remove


description = "Link your github account."

help = "**USAGE:**\n" \
       ":white_small_square:  `!github add <username/pofile link>`\n" \
       ":white_small_square:  `!github change <username/pofile link>`\n" \
       ":white_small_square:  `!github remove`\n" \
       ":white_small_square:  `!github list`\n" \
       ":white_small_square:  `!github get <@mention>`\n"


def ex(message, client):

    file = "gitlinks.save"
    links = {}

    if path.isfile(file):
        reader = open(file)
        for l in reader:
            links[l.split(":::")[0]] = l.split(":::")[1][:-1]
        reader.close()

    args = message.content.split(" ")[1:]

    if len(args) > 0:

        if args[0] == "add" or args[0] == "link":

            if len(args) < 2:
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=help))
                return

            if args[1].startswith("http") or args[1].startswith("www."):
                if not (args[1].startswith("http://github.com") or args[1].startswith("https://github.com") or args[1].startswith("www.github.com")):
                    yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description="Please enter a valid github URL or enter your github profile name."))
                    return
                profurl = args[1]
            else:
                profurl = "https://github.com/" + args[1]

            if links.keys().__contains__(message.author.id):
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("There is just an entry for this user!\n\n**[%s](%s)**\n\nChange the entry with `!github change <new url/username>` or remove it with `!github remove`." % (message.author.name, links[message.author.id]))))
                return
            f = open(file, "a")
            f.write(message.author.id + ":::" + profurl + "\n")
            f.close()
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Linked **[github profile](%s)** to user %s." % (profurl, message.author.mention))))


        if args[0] == "change" or args[0] == "edit":

            if len(args) < 2:
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=help))
                return

            if args[1].startswith("http") or args[1].startswith("www."):
                if not (args[1].startswith("http://github.com") or args[1].startswith("https://github.com") or args[1].startswith("www.github.com")):
                    yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description="Please enter a valid github URL or enter your github profile name."))
                    return
                profurl = args[1]
            else:
                profurl = "https://github.com/" + args[1]

            if not links.keys().__contains__(message.author.id):
                f = open(file, "a")
                f.write(message.author.id + ":::" + profurl + "\n")
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Linked **[github profile](%s)** to user %s." % (profurl, message.author.mention))))
            else:
                links[message.author.id] = profurl
                remove(file)
                f = open(file, "a")
                for k in links.keys():
                    f.write(k + ":::" + links[k])
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Changed link to **[github profile](%s)** of user %s." % (profurl, message.author.mention))))
            f.close()


        if args[0] == "remove" or args[0] == "delete":
            del links[message.author.id]
            remove(file)
            f = open(file, "a")
            for k in links.keys():
                f.write(k + ":::" + links[k])
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Removed link of user %s." % (message.author.mention))))
            f.close()


        if args[0] == "list" or args[0] == "all":
            out = ""
            for k in links.keys():
                out += ":white_small_square:  **%s:**  *%s*\n" % (discord.utils.get(message.server.members, id=k).name, links[k])
            yield from client.send_message(message.channel, "**GITHUB LINKS**\n\n" + out)


        if args[0] == "get":

            if len(args) < 2:
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=help))
                return

            membs = message.mentions

            if len(membs) < 1:
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description="Please mention user you want to get the github link from."))
                return

            if not links.keys().__contains__(membs[0].id):
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("Member %s has not linked his github profile yet." % membs[0].mention)))
                return

            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("**[%s](%s)**" % (membs[0].name, links[membs[0].id]))))

    else:
        yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=help))