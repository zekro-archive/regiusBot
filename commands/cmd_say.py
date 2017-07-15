import STATICS

description = "Say something ^^"


async def ex(message, client):

    msg = message.content.replace(STATICS.PREFIX + "say ", "")

    await client.send_message(message.channel, msg)
    await client.delete_message(message)
