import os
from colorama import Fore, Back, Style
import paramiko


def cmd1():
    ips = {"10.20.30.40": {"name": "Router"},
           "10.20.31.1": {"name": "R620"},
           "10.20.31.2": {"name": "EliteDesk"},
           "192.168.100.1": {"name": "Modem"},
           "google.com": {"name": "Internet Connectivity"},
           "192.168.100.2": {"name": "Fail test"}}

    results = ips

    for i in ips:
        response = os.system("ping -c 1 -i 0.5 -W 0.5 " + i)

        if response == 0:
            ips[i]["result"] = "up"
        else:
            ips[i]["result"] = "down"

    for key, value in ips.items():
        print(key + " (" + value["name"] + "): ", end="")
        if value["result"] == "up":
            print(Fore.GREEN, end="")
        else:
            print(Fore.RED, end="")
        print(value["result"] + Style.RESET_ALL)


def cmd2():
    return


def cmd3():
    return


def cmd4():
    return


print("Commands (enter number):")
print("1. Run tests")
print("2. Change local IP")
print("3. Restart pfSense")
print("4. Migrate pfSense to other server")

cmd1()

'''
while True:
    cmdnum = input("Which command would you like to run?")

    if cmdnum == 1:
        cmd1()
    elif cmdnum == 2:
        cmd2()
    elif cmdnum == 3:
        cmd3()
    elif cmdnum == 4:
        cmd4()
'''
