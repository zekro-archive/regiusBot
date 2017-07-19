import discord
import STATICS


description = "Create lmgtfy.com link"


async def ex(message, client):
    args = message.content.replace(STATICS.PREFIX + "lmgtfy ", "").split("|")
    if len(args) < 2:
        await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="**USAGE:**\n`!lmgtfy <link title>|<search query>`"))
    else:
        url = "http://lmgtfy.com/?q=" + args[1].replace(" ", "+")
        em = discord.Embed(title=args[0], url=url)
        await client.send_message(message.channel, embed=em)
        await client.delete_message(message)
