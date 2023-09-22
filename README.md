# NetworkDiagnosticBot
A handy script that can debug the network for me when I'm not there and I have to rely on non-technical users.

Current modes:
1. Get diagnostic information and run basic tests
2. Change local IP
3. Restart system
4. Open browser site


## Usage
This script is also intended to be run on a Windows machine, but through WSL (Ubuntu preferred). This allows access to some Linux tools in a fairly easy way, as well as still allowing access to Windows tools. 

You'll want to copy the `config.example.yaml` to `config.yaml`, then edit it to match your environment. Afterward, you can use Python 3 to run the script, such as via `python main.py`.

For convenience, you can also create a Windows shortcut to run this script. Open file explorer, then click Context Menu -> New -> Shortcut -> add the following: `wsl -- python /path/to/NetworkDiagnosticBot/main.py`.


## Limitations
In order for this script to be useful, modifications will be required. See the usage section for details. 

This script is currently primarily designed for IPv4 only, sorry IPv6 :(

Only ping and ssh tests are supported at this time. HTTP(s) might be added in the future. 
