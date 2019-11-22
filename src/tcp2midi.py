#!/bin/env python3
#$Id:$

"""
forwards tcp packets to midi-out
"""

__author__  = "gaul1@lifesim.de"
__version__ = "0.4"

import sys
import rtmidi
import socketserver
import os

#global 
#midiout = None
midiMsg = None
verbosity = 1

class MidiMessage:
  """
  holds midi message and the midi obj. only sender until yet.
  """
  data=[0]
  posWrite = 0
  midiobj = None
  midiports=[]
  
  # STATUS_4ByteMsg 
  # STATUS_3ByteMsg
  
  def __init__(self):
    self.reset()

  def status(self):
    return (self.data[0]>>4)

  def channel(self):
    return self.data[0] & 0xf

  def valid(self):
    return self.data[0] & 0x80 >0

  def feed(self, data):
    # if sys.version_info[0]==3:
      # data = data.encode()
    if isinstance(data, bytes):
      data = ord(data[0])
    if self.valid():
      self.data.append(data)
    else:
      if data & 0x80:
        self.data=[data]
    return len(self.data)

  def popMsg(self):
    d= self.data[:midiMsg.msgLen()]
    self.reset()
    return d

  def reset(self):
    self.data=[0]

  def msgLen(self):
    if self.status() == 0xf:
      return 4
    else:
      return 3
        
        
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    # midiMsg = None
    # midiout = None
    connected = 0

    def handle(self):
        global midiMsg, verbosity
        # self.request is the TCP socket connected to the client
        if not self.connected:
          self.connected = 1
          if verbosity:
            print("connection from: %s:%d to:%s:%d"%(self.client_address+self.server.server_address))
        data = self.request.recv(999)
        if not len(data):
          if verbosity:
            print("tcp in: empty packet. Probably connection closed.")
            self.connected = 0
          return
        if data[:3]==b"-v=":
          try:
            verbosity = int(data[3:])
            print("set verbosity to %d"%verbosity)
          except:
            pass
        if data[:7]==b"-LPorts":
          if verbosity:
            print("Get MIDI dev. List")
          self.request.sendall(listOfMidiPorts().encode())
        if verbosity>2:
          print("tcp in: " +str(data))
        for d in data:
          r = midiMsg.feed(d)
          r2= r and r>= midiMsg.msgLen()
          if r2:
            m=midiMsg.popMsg()
            if sys.version_info[1] == 8:
              m1 = b""
              for c in m:
                m1 += chr(c).encode()
              mm = rtmidi.MidiMessage.createSysExMessage(m1)
              midiMsg.midiobj.sendMessage(mm)
            else:
              midiMsg.midiobj.send_message(m)
            if verbosity >2:
              print("MIDI out: %s"%str(m))
        return
# endofclass


def usage():
  print("%s Version: %s by %s"%(sys.argv[0], __version__, __author__))
  print("use with param -p to get list of ports.") 
  print("else: tcp2midi midiport [tcp-port [tcp-hostname]]")
  print("else: -V: get version")
  print("else: -v=n set verbosity to n (0..5)")

def listOfMidiPorts():
  global midiMsg
  refreshMidiPorts()
  r = "List of Midi Ports:"+os.linesep
  n = 0
  for p in midiMsg.midiports:
    r += "%d. %s" % (n, p) +os.linesep
    n += 1
  r+="----"+os.linesep
  return r

def refreshMidiPorts():
  global midiMsg
  midiMsg.midiports=[]
  if sys.version_info[1] == 8:
    midiMsg.midiobj = rtmidi.RtMidiOut()
    for i in range(midiMsg.midiobj.getPortCount()):
      midiMsg.midiports.append(midiMsg.midiobj.getPortName(i))
  else:
    midiMsg.midiobj = rtmidi.MidiOut()
    midiMsg.midiports = midiMsg.midiobj.get_ports()

def main():
    global midiMsg, verbosity
    host,port = "localhost", 9999

    midiMsg = MidiMessage()
    refreshMidiPorts()
    midiportnum = 0
    verbosity=1
    
    le=len(sys.argv)
    if le <=1:
      usage()
      return
    if sys.argv[1]=="-V":
      print("Version: %s"%__version__)
      return
    try:
      if le >1:
        if sys.argv[1][0] != "-":
          midiportnum = int(sys.argv[1])
      if le >2:
        if sys.argv[2][0] != "-":
          port = int(sys.argv[2])
      if le >3:
        if sys.argv[3][0] != "-":
          host = sys.argv[3]
      for p in sys.argv:
        if p[:3] == "-v=":
          verbosity = int(p[3:])
    except:
      sys.argv[1]='-p'
    if sys.argv[1]=="-p":
      print("List of Midi Ports:")
      print(listOfMidiPorts())
      print("Call %s with the desired portnumber from the list above."%sys.argv[0])
      return
    if sys.version_info[1]==8:
      midiMsg.midiobj.openPort(midiportnum)
    else:
      midiMsg.midiobj.open_port(midiportnum)
      
    # Create the server, binding to localhost on port 9999
    if verbosity:
      print("Listening on ip:%s port:%d"%(host,port))
    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

if __name__ == "__main__":
  main()
#eof
