import discord
from bs4 import BeautifulSoup
import urllib
from utils import perms, twitter_api


description = "Stream announcing. (Only for zekro)"
DEVMODE = False


async def ex(message, client):

    author = message.author

    chanid = "308007834807697408" if not DEVMODE else "287535046762561536"
    channel = [c for c in message.server.channels if c.id == chanid][0]  # real: 308007834807697408  |  test: 287535046762561536

    if not perms.check_if_zekro(author):
        await client.send_message(author, embed=discord.Embed(color=discord.Color.red(), description="Sorry, this command is only available for zekro ;)"))
        await client.delete_message(message)
        return

    args = message.content.split(" ")[1:]
    img_url = args[0] if (len(args) > 0 and args[0] != "none") else "http://img.youtube.com/vi/XcNhbUv1Bdc/maxresdefault.jpg"
    msgcont = " ".join(args[1:]) if len(args) > 1 else ""

    await client.delete_message(message)

    page = urllib.request.urlopen("https://www.youtube.com/c/Zekrommaster110/live")
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find(id="eow-title").getText()[5:]

    em = discord.Embed()
    em.color = discord.Color.dark_gold()
    em.set_author(name="zekro - Coding/Tutorials", icon_url="https://yt3.ggpht.com/-K--pvHudDE4/AAAAAAAAAAI/AAAAAAAAAAA/9frZrI9aPDM/s88-c-k-no-mo-rj-c0xffffff/photo.jpg")
    em.description = "**Dev Stream ist online! :^)**\n\n" \
                     ":link:  [%s](https://www.youtube.com/c/Zekrommaster110/live)\n\n" \
                     "%s\n" % (title, msgcont)
    em.set_image(url=img_url)

    await client.send_message(channel, [r for r in message.server.roles if r.name == "Devs"][0].mention, embed=em)

    postToTwitter(img_url, msgcont)


def postToTwitter(img_url, msgcont):

    msg = msgcont + "\n\n" if len(msgcont) < 92 else ""

    content = "#DevStream ist online!\n\n%s" \
              "live.zekro.de" % msg

    try:
        twitter_api.post_media(content, img_url)
    except:
        twitter_api.post_media(content, "http://img.youtube.com/vi/XcNhbUv1Bdc/maxresdefault.jpg")
