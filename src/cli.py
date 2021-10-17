#!/usr/bin/env python3

# Client
import ssl
import sys
import time
import socket
import struct
import threading

import worker
import helper
import client

def main(argv):
  if (len(sys.argv) < 3):
    print("Usage: ./src/cli.py <host> <port> <port> ...")
    sys.exit(2)
  host = sys.argv[1]
  argfirstport = 2
  portlen = len(sys.argv) - argfirstport
  cl = [None]*portlen
  p = [None]*portlen
  i = argfirstport
  co = argfirstport
  actualports = 0
  while i < len(sys.argv):
    if sys.argv[i].isdigit():
      p[co - argfirstport] = int(sys.argv[i])
      co += 1
      actualports = co - argfirstport
    i += 1

  for i in range(actualports):
    try:
      cl[i] = client.Client(host, p[i])
      cl[i].setbigdata(b'D4T4B1GggR&B1gGgggR!'*10000)
      cl[i].start()
      time.sleep(2)
      cl[i].help.call_cworker()
      cl[i].join()
    except Exception:
      print("Could not connec to Server @ ", host, ":", p[i])

if __name__ == '__main__':
    main(sys.argv[1:])
