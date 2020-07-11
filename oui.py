import sys
from argparse import ArgumentParser
from os import stat, mkdir
from os.path import isfile, expanduser, isdir
from re import compile, match as rmatch, VERBOSE
from colorama import Fore, init
from requests import get as r_get


def download_oui_defs(fpath: str, force_dl=False) -> bool:
    # file exists and is not older than 1 week
    if (isfile(fpath) and stat(fpath).st_mtime > 604800) and not force_dl:
        print(f"{Fore.CYAN}Definitions exist and file is less than one week old, omitting download")
        return True
    else:
        if force_dl:
            print(f"{Fore.LIGHTRED_EX}Download forced, please wait...")
        else:
            print(f"{Fore.CYAN}Definitions not found or too old, downloading file, please wait...")
        r = r_get("http://standards-oui.ieee.org/oui.txt")
        if r.status_code == 200:
            with open(fpath, "wb") as fp:
                fp.write(r.content)
            return True
        else:
            print(f"{Fore.RED}Couldn't download oui definitions! HTTP status was {r.status_code}")
            return False


def lookup(fpath: str, mac: str) -> bool:
    vendor = mac[0:8].upper().replace(":", "-")
    pattern = compile(r"""^[0-9A-F]{2}    # match first octett at start of string
                           [-]            # match literal -
                           [0-9A-F]{2}    # match second otctett
                           [-]            # match literal -
                           [0-9A-F]{2}    # match third octett
                           .*$            # match until end of string""", flags=VERBOSE)

    with open(fpath, "rb") as fp_read:
        for line in fp_read:
            match = rmatch(pattern, line.decode('utf8'))
            if match:
                entry = match.group()
                entry = entry.split("\t")
                oui = entry[0].split()[0]
                name = entry[-1]
                if vendor == oui:
                    print(f"{Fore.GREEN}{mac} belongs to {name}")
                    return True
    print(f"{Fore.RED}Couldn't find oui {vendor}")
    return False


if __name__ == "__main__":
    init(autoreset=True)

    parser = ArgumentParser(description="oui.py: MAC vendor lookup")
    parser.add_argument("mac", help="The MAC address to process")
    parser.add_argument("--force", action="store_true", help="Force download of definitions file")
    parser.add_argument("--file", help="Override where file is stored and/or use this definition file")
    args = parser.parse_args()

    if args.file:
        f_path = args.file
    else:
        if not isdir(expanduser("~/.oui")):
            mkdir(expanduser("~/.oui"))
        f_path = expanduser("~/.oui/oui.txt")

    if not download_oui_defs(f_path, args.force):
        sys.exit(1)

    if not lookup(f_path, args.mac):
        sys.exit(1)

    sys.exit(0)



