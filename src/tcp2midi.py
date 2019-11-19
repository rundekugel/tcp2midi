#!/bin/env python3
#$Id:$

"""
forwards tcp packets to midi-out
"""

__author__  = "gaul1@lifesim.de"
__version__ = "0.1"

import sys
import rtmidi
import socketserver

#global 
#midiout = None
midiMsg = None

class MidiMessage:
  """
  holds midi message and the midi obj. only sender until yet.
  """
  data=[0]
  posWrite = 0
  midiobj = None
  
  # STATUS_4ByteMsg 
  # STATUS_3ByteMsg
  
  def __init__(self):
    d0=0
  def status(self):
    return (d[0]>>4) 
  def channel(self):
    return d[0] & 0xf
  def valid(self):
    return d[0] & 0x80 >0
  def feed(self, data):
    # if sys.version_info[0]==3:
      # data = data.encode()
    if self.valid:
      self.data.append(data)
    else:
      if data & 0x80:
        self.data=[data]
      else:
        self.data=[]
    return len(self.data)
  def reset(self):
    self.data=[]
  def msgLen(self):
    if self.status == 0xf:
      return 4
    else return 3
        
        
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    # midiMsg = None
    # midiout = None
    
    def handle(self):
        global midiMsg
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        r = midiMsg.feed(self.data)
        if r and r>= midiMsg.msgLen():
          midiMsg.midiobj.send_message(midiMsg.data[midiMsg[:midiMsg.msgLen())
        
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())

    # def __init__(self, p1=0,p2=0,p3=0,p4=0):
      # print("init with %s, %s, %s, %s"%(str(p1), str(p2), str(p3), str(p4)) )
      # super(socketserver.BaseRequestHandler, self).__init__()
    
def usage():
  print("use with param -p to get list of ports.") 
  print("else: tcp2midi midiport [tcp-port [tcp-hostname]]") 
    
def main():
    global midiout, midiMsg
    host,port = "localhost", 9999

    midiMsg = MidiMessage()
    midiMsg.midiobj = rtmidi.MidiOut()
    midiports = midiMsg.midiobj.get_ports()
    midiportnum = 0
    
    le=len(sys.argv)
    if le <=1:
      usage()
      return
    try:
      if le >1:
        midiportnum = int(sys.argv[1])
      if le >2:
        port = int(sys.argv[2])
      if le >3:
        host = sys.argv[3]
    except:
      print("List of Midi Ports:")
    #if sys.argv[1]=="-p":
      n=0
      for p in midiports:
        print("%d. %s"%(n, p.title()))
        n+=1
      print("Call %s with the desired portnumber from the list above."%sys.argv[0])
      return
    midiMsg.midiobj.open_port(midiportnum)
      
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

if __name__ == "__main__":
  main()
#eof
