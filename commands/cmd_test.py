import functions


def ex(message, client):
    yield from functions.send_join_pm(message.author, client)