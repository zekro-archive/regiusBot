from discord import Embed, Color, utils, ChannelType
from os import path, makedirs
from utils import perms


description = "Collect data about user for report purpose"
PREPATH = "/var/www/html/botstuff/rep/" # "REP/"


async def ex(message, client):

    if len([r for r in message.author.roles if r.name == "Moderator" or r.name == "Supporter"]) < 1:
         await client.send_message(message.channel, embed=Embed(description="You are not permitted to use this command!", color=Color.red()))
         return

    server = message.server
    victim = list(message.mentions)[0] if len(message.mentions) > 0 else server.get_member(message.content.split(" ")[1])

    if (victim == None):
        await client.send_message(message.channel, embed=Embed(description="Please enter a valid user!", color=Color.red()))
        return

    msg = await client.send_message(message.channel, embed=Embed(title="Collecting data...", description="Colelcting user data.."))

    spath = PREPATH + victim.id + "/messages"
    if not path.exists(spath):
        makedirs(spath)

    t = victim.joined_at
    jtime = "%s.%s.%s %s:%s:%s" % (str(t.day), str(t.month), str(t.year), str(t.hour), str(t.minute), str(t.second))

    userdata = {
        "Name": victim.name + "#" + victim.discriminator,
        "ID": victim.id,
        "Display Name": victim.display_name,
        "Roles": ", ".join([r.name for r in victim.roles]),
        "Joined At": jtime
    }

    with open(PREPATH + victim.id + "/userdata.txt", "w", -1, "utf-8") as f:
        for k, v in userdata.items():
            f.write("%s: %s\n" % (k, v))

    for c in server.channels:
        if c.type == ChannelType.text:
            await client.edit_message(msg, embed=Embed(title="Collecting data...", description="Searching in channel " + c.name))
            messages = []
            async for m in client.logs_from(c, limit=500):
                if m.author == victim:
                    messages.append(m)

            with open(spath + "/" + c.name + ".txt", "w", -1, "utf-8") as f:
                for m in messages:
                    t = m.timestamp
                    time = "%s.%s.%s %s:%s:%s" % (str(t.day), str(t.month), str(t.year), str(t.hour), str(t.minute), str(t.second))
                    f.write("[%s] '%s'\n" % (time, m.content))
    
    await client.edit_message(msg, embed=Embed(title="Collecting data...", description="[User data saved.](http://zekro.de/botstuff/rep/)"))