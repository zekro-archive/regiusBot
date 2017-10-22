from discord import Embed, Color


description = "Shows the link to the statistics page of the guild"


async def ex(message, client):
    await client.send_message(message.channel, embed=Embed(color=Color.gold(),
                                                           title="Discord Member Stats",
                                                           description="[STATICSTICS](http://s.zekro.de/dcstats)"))
    await client.delete_message(message)
