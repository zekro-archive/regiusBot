from utils import perms
from discord import Embed, Color
# import asyncio

description = "Kick the bot from servers (also just for zekro)"


async def ex(message, client):

    author = message.author
    content = message.content

    if not perms.check_if_zekro(author):
        await client.send_message(author, embed=Embed(color=Color.red(), description="Sorry, this command is only available for zekro ;)"))
        await client.delete_message(message)
        return

    serverid = content.split(" ")[1] if len(content.split(" ")[1:]) > 0 else None
    if serverid is None:
        print("[ERROR] Invalid argument.")
        return

    server = [s for s in client.servers if s.id == serverid]
    [(lambda x: print(x.id, x.id == serverid))(x) for x in client.servers]
    if len(server) < 1:
        print("[ERROR] Invalid server ID '%s'" % serverid)
        return
    server = server[0]

    # servername = server.name

    await client.leave_server(server)

    # TODO:
    # This mehtod will thow folloing error for some purpose...
    # FORBIDDEN (status code: 403): Missing Access
    # msg = await client.send_message(message.channel, embed=Embed(color=Color.red(), description="Knecht kicked himself successfully from server `%s`." % servername))
    # await asyncio.sleep(4)
    # await client.delete_message(msg)
