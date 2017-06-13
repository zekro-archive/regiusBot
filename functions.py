import discord
from discord import Member


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

    yield from client.send_message(member,
                                   "**Hey, " + member.name + "! Welcome on the \"DarkDevs\" Discord! :)**\n\n"
                                   "You automatically got assigned the role `Dev` by %s, I hope ^^\n"
                                   "Please now, go into the **%s** channel and type in `!dev` to get the roles witch languages you are writing in. The purpose behind that is that other users can "
                                   "directly see witch languages you are familiar with and on the other side to mention the role to speak to the members in this role in the chats.\n\n\n"
                                   "If you have some questions, look for online supporters or admins to ask for or ask the server owner (zekro) directly ;)\n\n"
                                   "**Currently online supporters:**\n\n%s\n\n"
                                   "Now, have a lot fun on the server! :)"
                                   % (discord.utils.get(member.server.members, id="272336949841362944").mention,
                                      discord.utils.get(member.server.channels, id="308153679716941825").mention,
                                      currently_online)
                                   )