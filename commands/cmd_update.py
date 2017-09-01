from utils import perms
from discord import Embed, Color
import STATICS

description = "Stream announcing. (Only for zekro)"
DEVMODE = False


async def ex(message, client):
    author = message.author

    if not perms.check_if_zekro(author):
        await client.send_message(author, embed=Embed(color=Color.red(), description="Sorry, this command is only available for zekro ;)"))
        await client.delete_message(message)
        return

    with open("changelog.txt") as f:
        content = ["".join(f.readlines())]


    em = Embed(color=Color.gold(), title="Update %s Changelogs" % STATICS.VERSION)

    if "#" in content[0]:
        content = content[0].split("#")[1:]
        for c in content:
            em.add_field(name=c.split("\n")[0], value="\n".join(c.split("\n")[1:]), inline=False)
    else:
        em.description = content[0]

    await client.send_message(message.channel, embed=em)
