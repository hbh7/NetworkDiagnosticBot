# NetworkDiagnosticBot
A handy script that can debug the network for me when I'm not there and I have to rely on non-technical users

List of the things to do:
```
Print this to user: 
Commands (enter number): 
1. Run tests
2. Change local IP
3. Restart pfSense
4. Migrate pfSense to other server

What to do for each (make a function):
1. Ping these ips, and verify ssh connectivity and print to user
    10.20.30.40 (Router)
    10.20.31.1 (R620)
    10.20.31.2 (EliteDesk) 
    192.168.100.1 (Modem) 
  print out current ip and whether it is in static or DHCP mode

2. Ask: 
  1. Set local IP to dynamic
    idk but find out haha
  2. Set local IP to static
    idk but set it to 10.20.29.99, 255.255.252.0, 10.20.30.40, 10.20.30.40, 8.8.8.8

3. Ask:
  1. Via pfSense
    10.20.30.40
    reboot (may need to go to shell first, not really sure hmm) 
  2. Via Proxmox
    ssh 10.20.31.2
    qm shutdown vmid
    sleep a while idk
    qm stop vmid
    qm start vmid

4. ssh 10.20.31.1
    restore vm from backup
    start vm
```
    
Eventually: 
Align output nicer
