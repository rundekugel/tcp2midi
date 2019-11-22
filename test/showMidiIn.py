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
import os

midiMsg = None

class MidiMessage:
  """
  holds midi message and the midi obj. only sender until yet.
  """
  data=[0]
  posWrite = 0
  midiobj = None
  midiports = []
  
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
# end of class


def usage():
  print("use with param -p to get list of ports.") 
  print("else: showMidiIn midiport")

def midiInCB(tuple, data=0):
  #print(tuple)
  m=tuple[0]
  print("Status: %02x, Note: %02x, Acc: %02x  # %s"%(
      m[0], m[1], m[2], str(tuple)))

def midiInCB1(msg):
  #print(msg)
  #print(msg.getChannel())
  m=msg.getRawData()
  #print(m)
  print("Status: %02x, Note: %02x, Acc: %02x  # %s"%(
      m[0], m[1], m[2], str(msg)))

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
  midiMsg = MidiMessage()
  midiMsg.midiports=[]
  if sys.version_info[1] == 8:
    midiMsg.midiobj = rtmidi.RtMidiIn()
    for i in range(midiMsg.midiobj.getPortCount()):
      midiMsg.midiports.append(midiMsg.midiobj.getPortName(i))
  else:
    midiMsg.midiobj = rtmidi.MidiIn()
    midiMsg.midiports = midiMsg.midiobj.get_ports()

def main():
    midiportnum = 0
    refreshMidiPorts()
    
    le=len(sys.argv)
    if le <=1:
      usage()
      return
    try:
      if le >1:
        midiportnum = int(sys.argv[1])
    except:
      sys.argv[1] = "-p"
    if sys.argv[1]=="-p":
      print(listOfMidiPorts())
      print("Call %s with the desired portnumber from the list above."%sys.argv[0])
      return
    if sys.version_info[1]==8:
      midiMsg.midiobj.openPort(midiportnum)
      midiMsg.midiobj.setCallback(midiInCB1)
    else:
      midiMsg.midiobj.open_port(midiportnum)
      midiMsg.midiobj.set_callback(midiInCB, 0)
    while 1:
      time.sleep(0.1)

if __name__ == "__main__":
  main()
#eof
