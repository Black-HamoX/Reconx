import os
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = r"""
 ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
 ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
 ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝
 ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗
 ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
 ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
"""

TAGLINE = "OSINT Reconnaissance Toolkit v1.0.0"
DEV_HANDLE = "@C5_72"
CHANNEL = "https://t.me/rootaccess_7"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}        {TAGLINE}")
    print(f"{Fore.GREEN}        Developer : {Fore.WHITE}{DEV_HANDLE}")
    print(f"{Fore.GREEN}        Channel   : {Fore.WHITE}{CHANNEL}")
    print(f"{Fore.CYAN}{'=' * 55}{Style.RESET_ALL}\n")


def print_info(msg):
    print(f"{Fore.BLUE}[*]{Style.RESET_ALL} {msg}")


def print_success(msg):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")


def print_error(msg):
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")


def print_warning(msg):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")


def print_section(title):
    print(f"\n{Fore.CYAN}{'=' * 55}")
    print(f"{Fore.CYAN}  {title}")
    print(f"{Fore.CYAN}{'=' * 55}{Style.RESET_ALL}")
