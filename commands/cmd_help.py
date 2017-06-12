import STATICS


def ex(message, client):
    yield from client.send_message(message.author, STATICS.helpText)
    yield from client.delete_message(message)
