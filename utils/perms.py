import discord
import STATICS


def check(member):
    if discord.utils.get(member.roles, name=STATICS.PERMS_ROLE_1) is None:
        return False
    return True


def check_if_zekro(member):
    return member.id == "221905671296253953"
