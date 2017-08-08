from discord import Embed, Color
from bs4 import BeautifulSoup
import urllib
from utils import perms

description = "Announcing video. (Only for zekro)"


async def ex(message, client):

    channel = [c for c in message.server.channels if c.id == "308007834807697408"][0]  # real: 308007834807697408  |  test: 287535046762561536
    author = message.author

    if not perms.check_if_zekro(author):
        await client.send_message(author, embed=Embed(color=Color.red(), description="Sorry, this command is only available for zekro ;)"))
        await client.delete_message(message)
        return

    args = message.content.split(" ")[1:] if len(message.content.split(" ")[1:]) > 0 else None
    if args is None:
        return

    vidurl = args[0]
    bs = BeautifulSoup(urllib.request.urlopen(vidurl).read(), "html.parser")

    title = bs.find("h1", {"class": "watch-title-container"}).find("span").getText()[5:-3]
    thumbnail = "http://img.youtube.com/vi/%s/maxresdefault.jpg" % vidurl[vidurl.index("watch?v=") + 8:]

    em = Embed(color=0xf75238)
    em.set_author(name="zekro - Coding/Tutorials", icon_url="https://yt3.ggpht.com/-K--pvHudDE4/AAAAAAAAAAI/AAAAAAAAAAA/9frZrI9aPDM/s88-c-k-no-mo-rj-c0xffffff/photo.jpg")
    em.set_image(url=thumbnail)
    em.description = "**Neues Video online! :^)**\n\n" \
                     ":link:  [%s](%s)" % (title, vidurl)

    await client.send_message(channel, [r for r in message.server.roles if r.name == "Devs"][0].mention, embed=em)
