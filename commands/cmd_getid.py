from discord import Embed, Color


description = "getting IDs"

async def ex(message, client):
    args = message.content.split()[1:]
    server = message.server
    print(len(args))
    if len(args) > 0:
        query = " ".join(args).lower()
        roles = ["%s  -  %s" % (r.name, r.id) for r in server.roles if query in r.name.lower()]
        chans = ["%s  -  %s" % (c.name, c.id) for c in server.channels if query in c.name.lower()]
        users = ["%s  -  %s" % (u.name, u.id) for u in server.members if query in u.name.lower()]

        s_roles = "\n".join(roles) if len(roles) > 0 else "*No roles found*"
        s_chans = "\n".join(chans) if len(chans) > 0 else "*No channels found*"
        s_users = "\n".join(users) if len(users) > 0 else "*No users found*"
        
        em = Embed(title="Elements found")
        em.add_field(name="Roles", value=s_roles, inline=False)
        em.add_field(name="Channels", value=s_chans, inline=False)
        em.add_field(name="Users", value=s_users, inline=False)

        await client.send_message(message.channel, embed=em)
    else:
        await client.send_message(message.channel, embed=Embed(description="**USAGE:**\n`!id <search string>`", color=Color.red()))