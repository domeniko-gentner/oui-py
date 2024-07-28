import sys
from argparse import ArgumentParser
from re import compile, match as rmatch, VERBOSE
from colorama import Fore, init
from requests import get as r_get
from pathlib import Path
from time import time


def download_oui_defs(def_file: Path, force_dl=False) -> bool:
    # check if file exists and is not older than 1 month
    time_diff = (time() - def_file.stat().st_mtime) - 2630000
    if not force_dl:
        if def_file.is_file() and int(time_diff) <= 0:
            print(f"{Fore.CYAN}Definitions exist and file is less than one week old, omitting download")
            return True
        else:
            if force_dl:
                print(f"{Fore.LIGHTRED_EX}Download forced, please wait...")
            else:
                print(f"{Fore.CYAN}Definitions not found or too old, downloading file, please wait...")
            r = r_get("https://standards-oui.ieee.org/oui/oui.txt", allow_redirects=False)
            if r.status_code == 200:
                with def_file.open('wb') as fp:
                    fp.write(r.content)
                return True
            else:
                print(f"{Fore.RED}Couldn't download oui definitions! HTTP status was {r.status_code}")
                return False


def lookup(def_file: Path, mac: str) -> bool:
    vendor = mac[0:8].upper().replace(":", "-")
    pattern = compile(r"""^[0-9A-F]{2}    # match first octett at start of string
                           -              # match literal -
                           [0-9A-F]{2}    # match second octett
                           -              # match literal -
                           [0-9A-F]{2}    # match third octett
                           .*$            # match until end of string""", flags=VERBOSE)

    with def_file.open("rb") as fp_read:
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


def main():
    init(autoreset=True)

    parser = ArgumentParser(description="oui.py: MAC vendor lookup")
    parser.add_argument("mac", help="The MAC address to process")
    parser.add_argument("--force", action="store_true", help="Force download of definitions file")
    args = parser.parse_args()

    home_path = Path("~/.oui")
    home_path = home_path.expanduser()
    home_path.mkdir(exist_ok=True)
    def_file = home_path / "oui.txt"

    if not download_oui_defs(def_file, args.force):
        sys.exit(1)

    if not lookup(def_file, args.mac):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()



