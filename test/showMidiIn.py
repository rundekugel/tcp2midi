#!/bin/env python3
#$Id:$

"""
show midi-in packets
"""

__author__  = "gaul1@lifesim.de"
__version__ = "0."

import sys
import rtmidi
import time

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
    data = ord(data)
    if self.valid():
      self.data.append(data)
    else:
      if data & 0x80:
        self.data=[data]
    return len(self.data)
  def reset(self):
    self.data=[0]
  def msgLen(self):
    if self.status() == 0xf:
      return 4
    else:
      return 3
        
def usage():
  print("use with param -p to get list of ports.") 
  print("else: showMidiIn midiport")

def midiInCB(tuple, data):
  #print(tuple)
  m=tuple[0]
  print("Status: %02x, Note: %02x, Acc: %02x  # %s"%(
      m[0], m[1], m[2], str(tuple)))

def main():
    # global  midiMsg
    # midiMsg = MidiMessage()

    midiobj = rtmidi.MidiIn()
    midiports =midiobj.get_ports()
    midiportnum = 0
    
    le=len(sys.argv)
    if le <=1:
      usage()
      return
    try:
      if le >1:
        midiportnum = int(sys.argv[1])
    except:
      print("List of Midi Ports:")
    #if sys.argv[1]=="-p":
      n=0
      for p in midiports:
        print("%d. %s"%(n, p.title()))
        n+=1
      print("Call %s with the desired portnumber from the list above."%sys.argv[0])
      return
    midiobj.open_port(midiportnum)
    midiobj.set_callback(midiInCB, 0)
    while 1:
      time.sleep(0.1)

if __name__ == "__main__":
  main()
#eof
