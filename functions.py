import discord


def get_members_msg(client):
    members = discord.utils.get(client.servers, id="307084334198816769").member_count
    members_online = []
    for m in discord.utils.get(client.servers, id="307084334198816769").members:
        if not m.status.__str__() == "offline":
            members_online.append(m)
    return "%s members (%s online) | !help" % (members, len(members_online))


def send_join_pm(member, client):

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

    yield from client.send_message(member,
                                   "**Hey, " + member.name + "! Welcome on the \"DarkDevs\" Discord! :)**\n\n"
                                   "You automatically got assigned the role `Dev` by %s, I hope ^^\n"
                                   "Please now, go into the **%s** channel and type in `!dev` to get the roles witch languages you are writing in. The purpose behind that is that other users can "
                                   "directly see witch languages you are familiar with and on the other side to mention the role to speak to the members in this role in the chats.\n\n\n"
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
                                      user_bots[2:])
                                   )