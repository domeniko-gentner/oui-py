from argparse import ArgumentParser
from colorama import Fore, init
from os.path import isfile
from os import stat
import requests
import re
import sys


def download_oui_defs(force_dl=False) -> bool:
    # file exists and is not older than 1 week
    if (isfile("oui.txt") and stat("oui.txt").st_mtime > 604800) and not force_dl:
        print(f"{Fore.CYAN}Definitions exists and is less than one week old, omitting download")
        return True
    else:
        if force_dl:
            print(f"{Fore.LIGHTRED_EX}Download forced, please wait...")
        else:
            print(f"{Fore.CYAN}Definitions not found or too old, downloading file, please wait...")
        r = requests.get("http://standards-oui.ieee.org/oui.txt")
        if r.status_code == 200:
            with open("oui.txt", "wb") as fp:
                fp.write(r.content)
            return True
        else:
            print(f"{Fore.RED}Couldn't download oui definitions!")
            return False


def parse_definitions() -> dict:
    result = dict()
    with open("oui.txt", "rb") as fp_read:
        for line in fp_read:
            match = re.match("^[0-9A-F_]{2}[-][0-9A-F_]{2}[-][0-9A-F_]{2} .*$", line.decode('utf8'))
            if match:
                entry = match.group()
                entry = entry.split("\t")
                oui = entry[0].split()[0]
                name = entry[-1]
                result[oui] = name
    return result


def lookup(macs: dict, mac: str) -> bool:
    mac = mac.upper()
    if mac[0:8] in macs:
        print(f"{Fore.GREEN}{mac} belongs to {macs[mac[0:8]]}")
        return True
    print(f"{Fore.RED}Couldn't find oui {mac[0:8]}")
    return False


if __name__ == "__main__":
    init(autoreset=True)

    parser = ArgumentParser(description="oui.py: MAC vendor lookup")
    parser.add_argument("mac", help="The MAC address to process")
    parser.add_argument("--force", action="store_true", help="Force download of definitions file")
    args = parser.parse_args()

    if not download_oui_defs(args.force):
        print(f"{Fore.RED}Something wen't wrong during the download")
        sys.exit(1)

    mac_arg = args.mac
    if mac_arg[2] == ":":
        mac_arg = mac_arg.replace(":", "-")

    if lookup(parse_definitions(), mac_arg):
        sys.exit(0)
    else:
        sys.exit(1)



