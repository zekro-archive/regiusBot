import discord


def get_members_msg(client):
    members = discord.utils.get(client.servers, id="307084334198816769").member_count
    members_online = []
    for m in discord.utils.get(client.servers, id="307084334198816769").members:
        if not m.status.__str__() == "offline":
            members_online.append(m)
    return "%s members (%s online) | !help" % (members, len(members_online))


def send_join_pm(member, client):
    yield from client.send_message(member,
                                   "**Hey, " + member.mention + "! Welcome on the Dark Devs Discord! :)**\n\n"
                                   "You automatically got assigned the role `Member` by zekroBot, I hope ^^\n"
                                   "Please now, go into the **`#commands`** channel and type in `!dev` to get the roles witch languages you are writing in. The purpose behind that is that other users can "
                                   "directly see witch languages you are familiar with and on the other side to mention the role to speak to the members in this role.\n\n"
                                   "If you have some questions, look for online supporters or admins to ask for or ask the server owner (zekro) directly ;)\n\n"
                                   "Now, have a lot fun on the server! :)"
                                   )