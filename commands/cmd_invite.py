from discord import Embed, Color, utils
from utils import functions


description = "Enter bot ID which the bot sends as invite link to zekro (Server Owner)"

last_invite = {}


async def ex(message, client):

    args = message.content.split()

    if len(args) > 1:
        global last_invite
        last_invite[args[1]] = message.author

        invite_receivers = [utils.get(message.server.members, id=uid) for uid in functions.get_settings()["roles"]["invite-receivers"]]
        for u in invite_receivers:
            await client.send_message(u, embed=Embed(
                color=Color.gold(),
                title="Bot invite from " + message.author.name,
                description="https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot" % args[1]))
            em = Embed(
                    colour=Color.green(),
                    description="[Invite link](https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot) "
                                "send to %s. One of them will (hopefully ^^) accept your invite as soon as possible.\n"
                                "**Please don't send multiple invite links! It can take a while until someone will accept the bot manually!**\n\n"
                                "**ATTENTION:**\nYou ned to set yout Bot as a **Public Bot** (see screenshot)!\n"
                                "Otherwise, we will not be able to add the bot to the server!"
                                % (args[1], ", ".join([m.mention for m in invite_receivers])))
            em.set_image(url="https://image.prntscr.com/image/R8AjJQ77R__Gg6HCnw9TeQ.png")
            await client.send_message(message.author, embed=em)
            await client.delete_message(message)

    else:
        await client.send_message(message.channel, embed=Embed(description="**USAGE:**\n`!invite <Bot ID>`\n*You can get your Bot ID from the [Discord Apps Panel](https://discordapp.com/developers/applications/me) from `Client ID`.*", color=Color.red()))