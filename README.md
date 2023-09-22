# NetworkDiagnosticBot
A handy script that can debug the network for me when I'm not there and I have to rely on non-technical users.


## Usage
This script is also intended to be run on a Windows machine, but through WSL (Ubuntu preferred). This allows access to some Linux tools in a fairly easy way, as well as still allowing access to Windows tools. 

You'll want to edit the config.env to match your environment. Then you can use Python 3 to run the script, such as via `python main.py`.

For convenience, you can also create a Windows shortcut to run this script. Open file explorer, then click Context Menu -> New -> Shortcut -> add the following: `wsl -- python /path/to/NetworkDiagnosticBot/main.py`.


## Limitations
In order for this script to be useful outside my specific use cases, modifications will be required. See the usage section for details. 

This script is designed for ipv4 only.

Only ping and ssh tests are supported at this time. HTTP(s) might be added in the future. 
