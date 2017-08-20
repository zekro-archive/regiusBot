from discord import Embed, Color, utils, Game
from utils import functions

description = "Add roles wich languages you write in."

customenabled = False


async def ex(message, client):

    author = message.author
    content = message.content
    channel = message.channel
    global customenabled

    if not utils.get(author.server.roles, name="Admin") in [r for r in author.roles]:
        await client.send_message(channel, embed=Embed(color=Color.red(), description="You dont have the permissions to use this command!"))
    else:
        args = " ".join(content.split()[1:])
        if customenabled and (args.startswith("off") or args.startswith("disable")):
            customenabled = False
            await client.send_message(channel, embed=Embed(description="Disbaled custom botmessage."))
            await client.change_presence(game=Game(name=functions.get_members_msg(client)))
        else:
            await client.send_message(channel, embed=Embed(description="%s changed bot message to `%s`." % (author.mention, args), color=Color.blue()))
            await client.change_presence(game=Game(name=args + " | !help"))
            customenabled = True
