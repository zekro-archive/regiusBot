import STATICS

description = "Say something ^^"


def ex(message, client):

    msg = message.content.replace(STATICS.PREFIX + "say ", "")

    yield from client.send_message(message.channel, msg)
    yield from client.delete_message(message)