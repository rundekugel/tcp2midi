# tcp2midi
Forward MIDI messages from TCP/IP to MIDI interface

use with:<br>
tcp2midi p [tcpportnumber [,local IP]]<br>
p=midi port number

user params:<br>
-V:   Version<br>
-v=n  set verbosity to n (must be last parameter)<br>
-p    get list of midi ports<br>

you can also retrieve list of midi-ports via tcp/ip to do this, send via tcp/ip:<br>
-LPorts

every messages will be truncated. if status messages with 0xFx they can be 4 bytes long, else all after byte 3 will be truncated.<br>
