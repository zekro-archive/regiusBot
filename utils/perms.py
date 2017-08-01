import discord
import STATICS


def check(member):
    if discord.utils.get(member.roles, name=STATICS.PERMS_ROLE_1) is None:
        return False
    return True
