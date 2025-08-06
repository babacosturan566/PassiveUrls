import os
import time
import shutil
import requests
import argparse
import subprocess
from datetime import datetime


parser = argparse.ArgumentParser(description="PassiveUrls: A passive URL extraction tool")

parser.add_argument("-d", type=str, required=True, help="Domain of the target (e.g., example.com)")
parser.add_argument("-po", action="store_true", help="Print the extracted URLs")

args = parser.parse_args()

# --- Colors ---
red     = "\033[31m"
blue    = "\033[34m"
green   = "\033[32m"
name_bg = "\033[48;5;235m"
gray_bg = "\033[48;5;237m"
reset   = "\033[0m"

def checkDependencies():
    # Check if 'uro' is installed
    if shutil.which("uro") is None:
        print(f"{blue}[INFO]{reset} 'uro' is not installed. Installing...")

        if shutil.which("pipx") is None:
            print(f"{blue}[INFO]{reset} 'pipx' is not installed. Installing pipx...")
            time.sleep(1)
            os.system("sudo apt install pipx -y")

        os.system("pipx install uro")
    time.sleep(1)


def banner():
    me = f"created by: " + name_bg + red + "NakuTenshi" + reset + reset
    print(fr"""
{blue}+-----------------------------------------------------------------------------+{reset}
{blue}|{reset}  _____              _           _    _      _                               {blue}|{reset}
{blue}|{reset} |  __ \            (_)         | |  | |    | |                              {blue}|{reset}
{blue}|{reset} | |__) |_ _ ___ ___ ___   _____| |  | |_ __| |___                           {blue}|{reset}
{blue}|{reset} |  ___/ _` / __/ __| \ \ / / _ \ |  | | '__| / __|                          {blue}|{reset}
{blue}|{reset} | |  | (_| \__ \__ \ |\ V /  __/ |__| | |  | \__ \ {me}   {blue}|{reset}
{blue}|{reset} |_|   \__,_|___/___/_| \_/ \___|\____/|_|  |_|___/ fuck this people         {blue}|{reset}
{blue}|{reset}                                                                             {blue}|{reset}
{blue}+-----------------------------------------------------------------------------+{reset}
""")


def main():
    os.system("clear")
    banner()
    checkDependencies()

    domain = args.d
    tool_path = os.path.expanduser("~/PassiveUrls")
    currentYear = datetime.now().year

    if not os.path.exists(tool_path):
        print(f"{blue}[INFO]{reset} Creating 'PassiveUrls' folder in home directory...")
        os.mkdir(tool_path)

    target_path = os.path.join(tool_path, domain)

    if not os.path.exists(target_path):
        print(f"{blue}[INFO]{reset} Creating target folder at: {target_path}")
        os.mkdir(target_path)

    log_path = os.path.join(target_path, "log.log")
    result_path = os.path.join(target_path, f"{domain}.txt")

    # --- Main Logic ---
    print(f"<------------------ {green}Status{reset} ------------------>")
    print(f"{blue}[INFO]{reset} Target: {red}{domain}{reset}")
    print(f"{blue}[INFO]{reset} Target path: {blue}{target_path}{reset}")
    if args.po:
        print(f"{blue}[INFO]{reset} Print URLs: {green}enabled{reset}")
    else:
        print(f"{blue}[INFO]{reset} Print URLs: {red}disabled{reset}")

    print(f"\n<------------------- {green}Logs{reset} ------------------->")
    print(f"{blue}[INFO]{reset} Sending request to {green}archive.org{reset}...")

    response = requests.get("https://web.archive.org/cdx/search/cdx", params={
        "url": domain,
        "matchType": "domain",
        "fl": "original",
        "from": currentYear,
        "to": currentYear
    })

    if response.status_code == 200:
        with open(log_path, "w") as f:
            f.write(response.text)

        result = subprocess.run(f"uro -i {log_path}", shell=True, capture_output=True, text=True)
        output = result.stdout
        error = result.stderr

        if not error:
            with open(result_path, "w") as f:
                f.write(output)

            if args.po:
                print(f"\n<------------------- {green}URLs{reset} ------------------->")
                print(output)

            print(f"{blue}[INFO]{reset} URLs successfully saved to: {green}file://{result_path}{reset}")
            os.remove(log_path)

        else:
            print(f"{red}[ERROR]{reset} An error occurred during URL filtering.")
            exit()

    else:
        print(f"{red}[ERROR]{reset} Failed to connect. Please check your internet connection.")
        exit()


# --- Entry Point ---
if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"{red}[ERROR]{reset} No internet connection. Please check your network.")
    except KeyboardInterrupt:
        print("\nBye :)")
        exit()
    except Exception as e:
        print(f"{red}[ERROR]{reset} Unexpected error: {e}")
