from bs4 import BeautifulSoup
import urllib


PREFIX = "!"
VERSION = "1.C00"
helpText = "__**Command list:**__\n\n"
PERMS_ROLE_1 = "Supporter"


def set_version():

    def _clean(inputstr):
        return inputstr.replace(" ", "").replace("\n", "")

    soup = BeautifulSoup(urllib.request.urlopen("https://github.com/zekroTJA/regiusBot/tree/dev"), "html.parser")
    commits_dev = _clean(soup.find("a", {"href": "/zekroTJA/regiusBot/commits/dev"}).find("span").getText())

    global VERSION
    VERSION = "1.C" + commits_dev


def set_prefix(devmode):
    global PREFIX
    PREFIX = "." if devmode else "!"
