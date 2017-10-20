from discord import Embed, Color
import STATICS
import datetime
import urllib
import json
from bs4 import BeautifulSoup

description = "Display info about the bot."
cmdcount = 0


async def ex(message, client):

    msg = await client.send_message(message.channel, embed=Embed(description="Collecting data..."))

    packages = ":white_small_square:   [discord.py](https://github.com/Rapptz/discord.py)\n" \
               ":white_small_square:   [request](https://pypi.python.org/pypi/requests)\n" \
               ":white_small_square:   [BeautifulSoup](https://github.com/waylan/beautifulsoup)\n" \
               ":white_small_square:   [gspread](https://github.com/burnash/gspread)\n" \
               ":white_small_square:   [giphypop](https://github.com/shaunduncan/giphypop)" \

    em = Embed(color=Color.gold(), description="This is a discord bot running on python 3.6 wich is only concipated to work for the `DARK DEVS` server.")
    em.title = "KnechtBot v." + STATICS.VERSION
    em.set_thumbnail(url=client.user.avatar_url)
    em.add_field(name="Current Version", value=STATICS.VERSION, inline=True)
    em.add_field(name="Commands", value=str(cmdcount), inline=True)
    em.add_field(name="Copyright", value="© %s zekro Development" % str(datetime.datetime.now().year), inline=False)
    em.add_field(name="Used 3rd Party Packages", value=packages, inline=False)
    em.add_field(name="GitHub Repository", value=get_github_content(), inline=False)
    # em.add_field(name="", value="", inline=False)
    # em.add_field(name="", value="", inline=False)
    # em.add_field(name="", value="", inline=False)

    await client.edit_message(msg, embed=em)


def get_github_content():

    def get_json(url):
        return json.loads(urllib.request.urlopen(url).read())

    def clean(inputstr):
        return inputstr.replace(" ", "").replace("\n", "")

    soup = BeautifulSoup(urllib.request.urlopen("https://github.com/zekroTJA/regiusBot/tree/dev"), "html.parser")
    commits_dev = clean(soup.find("a", {"href": "/zekroTJA/regiusBot/commits/dev"}).find("span").getText())

    soup = BeautifulSoup(urllib.request.urlopen("https://github.com/zekroTJA/regiusBot/tree/master"), "html.parser")
    commits_master = clean(soup.find("a", {"href": "/zekroTJA/regiusBot/commits/master"}).find("span").getText())
    branches = clean(soup.find("a", {"href": "/zekroTJA/regiusBot/branches"}).find("span").getText())
    contributors = clean(soup.find("a", {"href": "/zekroTJA/regiusBot/graphs/contributors"}).find("span").getText())

    return ":white_small_square:   **[Dev branch (latest)](https://github.com/zekroTJA/regiusBot/tree/dev)**\n" \
           ":white_small_square:   **[Master branch](https://github.com/zekroTJA/regiusBot/tree/master)**\n" \
           "```\n" \
           "Commits (Dev):     %s\n" \
           "Commits (Master):  %s\n" \
           "Branches:          %s\n" \
           "Contributors:      %s\n" \
           "```" % (commits_dev, commits_master, branches, contributors)
