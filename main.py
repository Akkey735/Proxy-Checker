import os
import sys
import time
import yaml # pip install pyyaml
import httpx # pip install httpx
import numpy # pip install numpy
import colorama # pip install colorama
import pyfiglet # pip install pyfiglet
import threading

colorama.init(convert=True)

working_proxies = []
no_working_proxies = []
checked_proxies = []
threads = []
running = False

def update_title():
    while running:
        os.system(f"title Proxy Checker / Checked: {str(len(checked_proxies))} / Working: {str(len(working_proxies))} / Not Working: {str(len(no_working_proxies))}")
    os.system("title Proxy Checker")
    return

def check(proxies, timeout, raw_ip):
    global working_proxies
    global no_working_proxies
    global checked_proxies
    for proxy in proxies:
        if proxy in checked_proxies:
            continue
        try:
            proxies_config = {
                "http://": f"http://{proxy}",
                "https://": f"http://{proxy}"
            }
            response = httpx.get("https://api.ipify.org", proxies=proxies_config, timeout=(timeout, timeout))
            if response.text != raw_ip:
                working_proxies.append(proxy)
            else:
                no_working_proxies.append(proxy)
        except:
            no_working_proxies.append(proxy)
        checked_proxies.append(proxy)
    return

def main():
    global threads
    global running
    update_title()
    print(colorama.Fore.LIGHTGREEN_EX + pyfiglet.figlet_format("CHECKER") + colorama.Fore.RESET)
    time.sleep(1)
    if not os.path.exists("config.yml"):
        print(colorama.Fore.RED + "config.yml does not exist." + colorama.Fore.RESET)
        return
    with open("config.yml", "r", encoding="utf-8", errors="ignore") as file:
        config = yaml.safe_load(file)
    max_threads = config["threads"]
    if not max_threads >= 1:
        print(colorama.Fore.RED + "The maximum number of threads must be set to at least 1." + colorama.Fore.RESET)
        return
    print(colorama.Fore.YELLOW + "Checking for live ip." + colorama.Fore.RESET)
    raw_ip = "0.0.0.0"
    try:
        raw_ip = httpx.get("https://api.ipify.org")
    except:
        print(colorama.Fore.RED + "An error occurred while retrieving the raw ip." + colorama.Fore.RESET)
        return
    proxy_path = input("Proxy File: ")
    if not os.path.exists(proxy_path):
        print(colorama.Fore.RED + "The specified path does not exist." + colorama.Fore.RESET)
        return
    elif not os.path.isfile(proxy_path):
        print(colorama.Fore.RED + "The path specified appears to be a folder, not a file." + colorama.Fore.RESET)
        return
    with open(proxy_path, "r", encoding="utf-8", errors="ignore") as file:
        proxies = file.read().split("\n")
    if not len(proxies) >= 1:
        print(colorama.Fore.RED + "At least one proxy must be specified." + colorama.Fore.RESET)
        return
    print(colorama.Fore.GREEN + f"{str(len(proxies))} proxy loaded.")
    running = True
    threading.Thread(target=update_title).start()
    fixed_proxies = numpy.array_split(proxies, max_threads)
    for check_proxies in fixed_proxies:
        check_thread = threading.Thread(target=check, args=(list(check_proxies), float(config["timeout"]), raw_ip,))
        threads.append(check_thread)
        check_thread.start()
    for check_thread in threads:
        check_thread.join()
    running = False
    print(colorama.Fore.GREEN + "Check is complete." + colorama.Fore.RESET)
    print(colorama.Fore.LIGHTCYAN_EX + ">> " + colorama.Fore.GREEN + f"Working: {str(len(working_proxies))}" + colorama.Fore.LIGHTCYAN_EX + " | " + colorama.Fore.RED + f"Not Working: {str(len(no_working_proxies))}" + colorama.Fore.LIGHTCYAN_EX + " <<" + colorama.Fore.RESET)
    with open("working_proxies.txt", "w", encoding="utf-8") as file:
        file.write("{0}".format("\n".join(working_proxies)))
        file.close()
    print(colorama.Fore.GREEN + "A working proxy has been saved in working_proxies.txt." + colorama.Fore.RESET)

if __name__ == "__main__": # Determine if it is not called as a library
    main()
    sys.exit()
else:
    print("It cannot be called and used as an external file.")
    sys.exit()