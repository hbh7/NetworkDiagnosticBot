import os
from colorama import Fore, Back, Style
import paramiko
import socket
import subprocess
from simple_term_menu import TerminalMenu
from tabulate import tabulate


def cmd1():

    # IP Address Information
    proc = subprocess.Popen("ipconfig.exe /all", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    # Find physical ethernet adapters
    print("Current IP Information:")
    printout = False
    out = out.decode("utf-8").split('\n')
    targetData = [
        "Description",
        "Physical Address",
        "DHCP Enabled",
        "Autoconfiguration Enabled",
        "IPv4 Address",

    ]
    for line in out:
        if "Ethernet adapter Ethernet" in line:
            printout = True
        elif len(line) > 0 and line[0] != " " and line[0] != "\r":
            printout = False

        if printout:
            if [keyword for keyword in targetData if(keyword in line)]:
                print(line)


    #print("program output:", out)
    #print(type(out))
    #parts = out.decode("utf-8").split('\n')
    #print(parts)
    #print("Current IP Address: ")


    # Ping Test
    ips = {
        "10.20.32.1": {"name": "Router"},
        "10.20.32.99": {"name": "EliteDesk"},
        "10.20.31.1": {"name": "VPN Test (Node5)"},
        "8.8.8.8": {"name": "Internet Connectivity"},
        "google.com": {"name": "DNS + Internet Connectivity"}
    }

    for i in ips:
        # Linux only: Ping 3 times, .2 seconds between each try, wait a half second for each reply.
        # Response = 0 if all succeeded, 1 if some are missing, 2 for other errors.
        #response = os.system("ping -c 3 -W 0.5 " + i)
        proc = subprocess.Popen("ping -c 3 -W 0.5 -i 0.2 " + i, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        returnCode = proc.returncode
        #print("program output:", out)

        if returnCode == 0:
            ips[i]["result"] = "up"
        else:
            ips[i]["result"] = "down"

    tableData = []
    for key, value in ips.items():
        row = [key, value["name"]]
        #print(key + " (" + value["name"] + "): ", end="")
        if value["result"] == "up":
            row.append(Fore.GREEN + value["result"] + Style.RESET_ALL)
        else:
            row.append(Fore.RED + value["result"] + Style.RESET_ALL)
            #print(Fore.RED, end="")
        #print()
        tableData.append(row)


    # display table
    col_names = ["IP", "Alias", "Ping Result"]
    print(tabulate(tableData, headers=col_names, tablefmt="fancy_grid"))

    print()



def cmd2():
    return


def cmd3():
    return


def cmd4():
    return


if __name__ == "__main__":

    print("Network Diagnostic Bot")

    options = [
        "[1] Run tests",
        "[2] Change local IP",
        "[3] Restart opnSense",
        "[4] Restart Elitedesk",
        "[5] Exit"
    ]
    terminal_menu = TerminalMenu(options, title="Options:")

    while True:
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            cmd1()
        elif menu_entry_index == 1:
            cmd2()
        elif menu_entry_index == 2:
            cmd3()
        elif menu_entry_index == 3:
            cmd4()
        elif menu_entry_index == 4:
            break
        else:
            break

