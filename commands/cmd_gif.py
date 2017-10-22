import giphypop
import json
from discord import Embed, Color

client = None

description = "Send gifs from giphy."

helpmsg = "**Usage:**\n`!gif <search query> (<index>)`"


async def ex(message, client):
    
    if len(message.content.split()[1:]) < 1:
        await client.send_message(message.channel, embed=Embed(color=Color.red(), description=helpmsg))
        return

    msg = await client.send_message(message.channel, "Collecting data...")
    await client.delete_message(message)

    with open("general_settings.json") as f:
        key = json.load(f)["secrets"]["giphy"]

    g = giphypop.Giphy(api_key=key)
    argsstr = " ".join(message.content.split()[1:])

    search = argsstr[:argsstr.index("-")] if " -" in argsstr else argsstr
    index = int(argsstr[argsstr.index("-") + 1:]) if " -" in argsstr else 0

    await client.edit_message(msg, [x for x in g.search(search)][index])