description = "Edit bot message"

perm = 2

async def ex(message, client):
    args = message.content.split()[1:]

    if len(args) < 2: 
        return

    msgid = args[0]
    cont = message.content[len(message.content.split()[0]) + len(msgid) + 2:]

    async for m in client.logs_from(message.channel, limit=100):
        if m.id == msgid:
            await client.edit_message(m, cont)

    await client.delete_message(message)
    