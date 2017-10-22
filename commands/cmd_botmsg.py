from discord import Embed, Color, Game
from utils import functions

description = "Add roles wich languages you write in."

perm = 2

customenabled = False

async def ex(message, client):

    author = message.author
    content = message.content
    channel = message.channel
    global customenabled


    args = " ".join(content.split()[1:])
    if customenabled and (args.startswith("off") or args.startswith("disable")):
        customenabled = False
        await client.send_message(channel, embed=Embed(description="Disbaled custom botmessage."))
        await client.change_presence(game=Game(name=functions.get_members_msg(client)))
    else:
        await client.send_message(channel, embed=Embed(description="%s changed bot message to `%s`." % (author.mention, args), color=Color.blue()))
        await client.change_presence(game=Game(name=args + " | !help"))
        customenabled = True
