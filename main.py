import asyncio
import discord
from discord import Embed
from discord import Member
from discord import Message
from discord import Role
from discord import Server
from discord import User
from discord.ext import commands

import SECRETS

client = discord.Client()


# LISTENER

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')


@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.add_roles(member, discord.utils.get(member.server.roles, name="Devs"))
    yield from client.send_message(member,   "**Hey, " + member.name + "!**\n\n"
                                        "Welcome on our Discord Dev Server! You automatically got "
                                        "assigned the role *Devs*.\n"
                                        "Use the command `-dev` to get the languages you code in as roles for better"
                                        "conversations ^^\n\nSo much for that, have fun on the server! :)")


@client.event
@asyncio.coroutine
def on_message(message: Message):
    if message.author == client.user:
        return

    if (message.content.startswith("!info")):
        em = discord.Embed(title='Info', description='Python Discord Bot by zekro. \n© 2017 zekro Development', colour=discord.Color.green())
        yield from client.send_message(message.channel, embed=em)


client.run(SECRETS.token)
