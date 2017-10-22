import discord
import STATICS
import json


with open("general_settings.json") as f:
    settings = json.load(f)


lvl1 = settings["perms"]["1"]
lvl2 = settings["perms"]["2"]
lvl3 = settings["perms"]["3"]


def get(memb):
    lvl = [0]
    for r in memb.roles:
        if r.name in lvl3:
            lvl.append(3)
        elif r.name in lvl2:
            lvl.append(2)
        elif r.name in lvl1:
            lvl.append(1)
    return max(lvl)


def checklvl(memb, lvl):
    return get(memb) >= lvl


def check(member):
    if discord.utils.get(member.roles, name=STATICS.PERMS_ROLE_1) is None:
        return False
    return True


def check_if_zekro(member):
    return member.id == "221905671296253953"
