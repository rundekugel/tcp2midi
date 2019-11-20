# tcp2midi
Forward MIDI messages from TCP/IP to MIDI interface

use with:
tcp2midi p [tcpportnumber [,local IP]]
p=midi port number


user params:
-V:   Version
-v=n  set verbosity to n (must be last parameter)
-p    get list of midi ports

you can also retrieve list of midi-ports via tcp/ip to do this, send via tcp/ip:
-LPorts

every messages will be truncated. if status messages with 0xFx they can be 4 bytes long, else all after byte 3 will be truncated.
