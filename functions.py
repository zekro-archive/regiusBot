import discord


async def discord_add_from_pm():
    if args[1].startswith("http") or args[1].startswith("www."):
        if not (args[1].startswith("http://github.com") or args[1].startswith("https://github.com") or args[1].startswith("www.github.com")):
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(),
                                                                           description="Please enter a valid github URL or enter your github profile name."))
            return
        profurl = args[1]
    else:
        profurl = "https://github.com/" + args[1]

    if links.keys().__contains__(message.author.id):
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
            "There is just an entry for this user!\n\n**[%s](%s)**\n\nChange the entry with `!github change <new url/username>` or remove it with `!github remove`." % (
                message.author.name, links[message.author.id]))))
        return
    f = open(file, "a")
    f.write(message.author.id + ":::" + profurl + "\n")
    f.close()
    await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=(
            "Linked **[github profile](%s)** to user %s." % (profurl, message.author.mention))))


def get_members_msg(client):
    members = discord.utils.get(client.servers, id="307084334198816769").member_count
    members_online = []
    for m in discord.utils.get(client.servers, id="307084334198816769").members:
        if not m.status.__str__() == "offline":
            members_online.append(m)
    return "%s members (%s online) | !help" % (members, len(members_online))


async def send_join_pm(member, client):

    currently_online = ""
    for m in member.server.members:
        if not m.status.__str__() == "offline":
            if m.roles.__contains__(discord.utils.get(m.server.roles, name="Supporter")):
                currently_online += ":white_small_square:  " + m.mention + "\n"

    super_bots = ""
    user_bots = ""
    for b in member.server.members:
        if b.roles.__contains__(discord.utils.get(m.server.roles, name="Super Bots (zekro)")):
            super_bots += ", " + b.mention
        elif b.roles.__contains__(discord.utils.get(m.server.roles, name="User Bots")):
            user_bots += ", " + b.mention

    await client.send_message(member,
                              "**Hey, " + member.name + "! Welcome on the \"DarkDevs\" Discord! :)**\n\n"
                              "You automatically got assigned the role `Dev` by %s, I hope ^^\n"
                              "Please now, go into the **%s** channel and type in `!dev` to get the roles witch languages you are writing in. The purpose behind that is that other users can "
                              "directly see witch languages you are familiar with and on the other side to mention the role to speak to the members in this role in the chats. Also please link your github "
                              "profile (if existing) with the command `!github add <link or username>`.\n\n\n"
                              "After that, you can write a little bit about yourself in channel %s. :)\n\n\n"
                              "If you have some questions, look for online supporters or admins to ask for or ask the server owner (zekro) directly ;)\n\n"
                              "**Currently online supporters:**\n\n%s\n\n"
                              "Some information about the bots on this server:\n\n"
                              "**Super bots:**  %s\n"
                              "**User bots:**  %s\n\n"
                              "Use command `-help` to get command list from **zekroBot** and use `!help` to get information about **me (Knecht)**.\n\n\n"
                              "Now, have a lot fun on the server! :)"
                              % (discord.utils.get(member.server.members, id="272336949841362944").mention,
                                 discord.utils.get(member.server.channels, id="308153679716941825").mention,
                                 discord.utils.get(member.server.channels, id="309805161193406465").mention,
                                 currently_online,
                                 super_bots[2:],
                                 user_bots[2:]))


async def supp_add(before, after, client):

    message_id = "334299368079360000"
    channel = discord.utils.get(list(client.servers)[0].channels, name="welcome")
    message = await client.get_message(channel, message_id)

    if len(list(filter(lambda r: r.name == "Supporter", before.roles))) == 0 and len(list(filter(lambda r: r.name == "Supporter", after.roles))) == 1:
        content = ":bookmark:   **Supporters**\n\n"
        for m in after.server.members:
            if len(list(filter(lambda r: r.name == "Supporter", m.roles))) == 1:
                content += ":white_small_square:  " + m.mention + "\n"
        await client.edit_message(message, content)
