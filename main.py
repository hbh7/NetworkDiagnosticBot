from colorama import Fore, Style
import subprocess
from simple_term_menu import TerminalMenu
from tabulate import tabulate
import yaml


def getDiagnosticInfo(config):
    # IP Address Information
    proc = subprocess.Popen("ipconfig.exe /all", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    # Find physical ethernet adapters
    print("Current IP Information:")
    adapterPrintout = False
    informationPrintout = False
    out = out.decode("utf-8").split('\n')
    adapterTypes = config['ipconfig']['adapter_types']
    desiredFields = config['ipconfig']['desired_fields'] + adapterTypes
    for line in out:
        # Check for desired adapter type and enable printing if found
        if any(item in line for item in adapterTypes):
            print()
            adapterPrintout = True
        elif len(line) > 0 and line[0] != " " and line[0] != "\r":
            adapterPrintout = False

        if adapterPrintout:
            # Only print lines that match what we want, including follow-up lines
            if [keyword for keyword in desiredFields if (keyword in line)]:
                informationPrintout = True
                print(line)
            elif informationPrintout and len(line) >= 4 and line[3] == " ":
                print(line)
            else:
                informationPrintout = False

    # Load systems from config file
    systems = config['ping']['systems']

    # Start ping and connectivity tests
    print("\nRunning ping and connectivity tests...")
    for system in systems:
        # Ping Test
        # Linux only: Ping 3 times, .2 seconds between each try, wait a half second for each reply.
        # Response = 0 if all succeeded, 1 if some are missing, 2 for other errors.
        proc = subprocess.Popen("ping -c 3 -W 0.5 -i 0.2 " + system["ip"], stdout=subprocess.PIPE, shell=True)
        proc.communicate()
        returnCode = proc.returncode

        if returnCode == 0:
            system["ping_result"] = "up"
        else:
            system["ping_result"] = "down"
        print(".", end="")  # Status indicator

        # SSH Test
        if system["connectivity_test"] == "ssh":
            proc = subprocess.Popen("nc -w 2 " + system["ip"] + " 22", stdout=subprocess.PIPE, shell=True)
            proc.communicate()
            returnCode = proc.returncode

            if returnCode == 0:
                system["connectivity_result"] = "SSH up"
            else:
                system["connectivity_result"] = "SSH down"
        print(".", end="")  # Status indicator

    # Reformat into something we can display nicely
    tableData = []
    for system in systems:
        row = [system["ip"], system["name"]]
        if system["ping_result"] == "up":
            row.append(Fore.GREEN + system["ping_result"] + Style.RESET_ALL)
        else:
            row.append(Fore.RED + system["ping_result"] + Style.RESET_ALL)
        if "connectivity_result" in system:
            if "up" in system["connectivity_result"]:
                row.append(Fore.GREEN + system["connectivity_result"] + Style.RESET_ALL)
            else:
                row.append(Fore.RED + system["connectivity_result"] + Style.RESET_ALL)
        else:
            row.append(Fore.YELLOW + "not tested" + Style.RESET_ALL)
        tableData.append(row)

    # Display table of results
    col_names = ["IP", "Alias", "Ping Result", "Connectivity Result"]
    print()
    print(tabulate(tableData, headers=col_names, tablefmt="fancy_grid"))

    print()


def changeIp(config):
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
    if interface_number is not None and 0 <= interface_number < len(options):
        # Prompt to select static IP or DHCP mode
        options = ["[1] DHCP (Normal)", "[2] Static (Debug)"]
        terminal_menu = TerminalMenu(options, title="Select Mode:")
        mode = terminal_menu.show()

        # Validate selection
        if mode is not None and 0 <= mode < len(options):
            if mode == 0:
                # Set to DHCP
                proc = subprocess.Popen('netsh.exe interface ipv4 set address name="' + tableData[interface_number][1]
                                        + '" source=dhcp', stdout=subprocess.PIPE, shell=True)
            else:
                # Set to Static
                proc = subprocess.Popen('netsh.exe interface ipv4 set address name="' + tableData[interface_number][1]
                                        + '" static ' + config["static_local_ip"]["ip"]
                                        + ' ' + config["static_local_ip"]["mask"]
                                        + ' ' + config["static_local_ip"]["gateway"], stdout=subprocess.PIPE,
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


def restart_system(ip, username):
    proc = subprocess.Popen("ssh " + username + "@" + ip + " -t 'reboot'", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode("utf-8").split('\n')
    for line in out:
        print(line)
    return


def main():
    print("Network Diagnostic Bot")

    # Read configuration file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Build menu of options
    options = [
        "[1] Get diagnostic information and run basic tests",
        "[2] Change local IP"
    ]
    option_number = 3
    for system in config["restart"]["systems"]:
        options.insert(option_number - 1, f"[{option_number}] Restart {system['name']}")
        option_number += 1
    options.append("[" + str(option_number) + "] Exit")

    # Display menu
    terminal_menu = TerminalMenu(options, title="Main Menu Options:")
    while True:
        print("------------------------------------------------------")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            getDiagnosticInfo(config)
        elif menu_entry_index == 1:
            changeIp(config)
        elif 1 < menu_entry_index < option_number - 1:
            restart_system(config["restart"]["systems"][menu_entry_index - 4]["ip"],
                           config["restart"]["systems"][menu_entry_index - 4]["username"])
        else:
            break


if __name__ == "__main__":
    main()
