import os
from colorama import Fore, Back, Style
import paramiko
import socket
import subprocess
from simple_term_menu import TerminalMenu
from tabulate import tabulate


def getDiagnosticInfo():
    # IP Address Information
    proc = subprocess.Popen("ipconfig.exe /all", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    # Find physical ethernet adapters
    print("Current IP Information:")
    adapterPrintout = False
    informationPrintout = False
    out = out.decode("utf-8").split('\n')
    targetData = [
        "Ethernet adapter Ethernet",
        "Description",
        "Physical Address",
        "DHCP Enabled",
        "Autoconfiguration Enabled",
        #"IPv6 Address",
        "IPv4 Address",
        #"Lease Obtained",
        #"Lease Expires",
        "Subnet Mask",
        "Default Gateway",
        "DHCP Server",
        "DNS Servers",

    ]
    for line in out:
        if "Ethernet adapter Ethernet" in line:
            adapterPrintout = True
        elif len(line) > 0 and line[0] != " " and line[0] != "\r":
            adapterPrintout = False

        if adapterPrintout:
            # Only print lines that match what we want, including follow-up lines
            if [keyword for keyword in targetData if (keyword in line)]:
                informationPrintout = True
                print(line)
            elif informationPrintout and len(line) >= 4 and line[3] == " ":
                print(line)
            else:
                informationPrintout = False


    #print("program output:", out)
    #print(type(out))
    #parts = out.decode("utf-8").split('\n')
    #print(parts)

    # Ping Test
    print("Running ping tests...")
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


def changeIp():
    # Gather list of interfaces and details
    proc = subprocess.Popen("netsh.exe interface ipv4 show config", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode("utf-8").split('\n')

    # Format interface information into a table and selectable menu
    tableData = []
    options = []
    index = 1
    row = []
    adapterWanted = False
    for line in out:
        if "Configuration for" in line and "Ethernet" in line and "vEthernet" not in line:
            row.append(index)
            row.append(line.split('"')[1])
            adapterWanted = True

        elif adapterWanted and ("DHCP enabled" in line or "IP Address" in line or "Default Gateway" in line):
            row.append(line.split(" ")[-1].strip("\r"))

        elif adapterWanted and "Subnet Prefix" in line:
            row.append(line.split(" ")[-3])

        elif adapterWanted and len(line) == 1 and line[0] == "\r":
            tableData.append(row)
            row = []
            adapterWanted = False
            index += 1
            options.append("[" + str(tableData[-1][0]) + "] " + tableData[-1][1])
    col_names = ["Number", "Adapter Name", "DHCP Enabled?", "IP Address", "Subnet Prefix", "Default Gateway"]
    print(tabulate(tableData, headers=col_names, tablefmt="fancy_grid"))

    # Print out menu to select adapter
    terminal_menu = TerminalMenu(options, title="Select Adapter:")
    interface_number = terminal_menu.show()

    # Validate selection
    if 0 <= interface_number < len(options):
        # Prompt to select static IP or DHCP mode
        options = ["[1] DHCP (Normal)", "[2] Static (Debug)"]
        terminal_menu = TerminalMenu(options, title="Select Mode:")
        mode = terminal_menu.show()

        # Validate selection
        if 0 <= mode < len(options):
            # Make the (right) change
            if mode == 0:
                # Set to DHCP
                proc = subprocess.Popen('netsh.exe interface ipv4 set address name="' + tableData[interface_number][1]
                                        + '" source=dhcp', stdout=subprocess.PIPE, shell=True)
            else:
                # Set to Static
                # TODO: Have this be config driven
                proc = subprocess.Popen('netsh.exe interface ipv4 set address name="' + tableData[interface_number][1]
                                        + '" static 10.20.32.82 255.255.255.0 10.20.32.1', stdout=subprocess.PIPE,
                                        shell=True)
            (out, err) = proc.communicate()
            out = out.decode("utf-8").split('\n')
            if out == ["\r", ""] or out == ['DHCP is already enabled on this interface.\r', '\r', '']:
                print("IP address changed successfully.")
            else:
                print("Something went wrong:", out)

        else:
            print("Invalid option, please try again.")

    else:
        print("Invalid option, please try again.")


def cmd3():
    return


def cmd4():
    return


if __name__ == "__main__":

    print("Network Diagnostic Bot")

    options = [
        "[1] Get diagnostic information and run basic tests",
        "[2] Change local IP",
        "[3] Restart opnSense",
        "[4] Restart Elitedesk",
        "[5] Exit"
    ]
    terminal_menu = TerminalMenu(options, title="Main Menu Options:")

    while True:
        print("------------------------------------------------------")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            getDiagnosticInfo()
        elif menu_entry_index == 1:
            changeIp()
        elif menu_entry_index == 2:
            cmd3()
        elif menu_entry_index == 3:
            cmd4()
        elif menu_entry_index == 4:
            break
        else:
            break
