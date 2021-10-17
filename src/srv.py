#!/usr/bin/env python3

# Server
import ssl
import sys
import time
import signal
import socket
import struct
import threading

import worker
import helper
import db
import serversocket
import server

class ServiceExit(Exception):
  pass

def service_shutdown(signum, frame):
  raise ServiceExit

def main(argv):
  if (len(sys.argv) < 3):
    print("Usage: ./src/srv.py <host> <port> <port> ...")
    sys.exit(2)
  host = sys.argv[1]
  argfirstport = 2
  portlen = len(sys.argv) - argfirstport
  sr = [None]*portlen
  ss = [None]*portlen
  p = [None]*portlen
  i = argfirstport
  co = argfirstport
  actualports=0
  while i < len(sys.argv):
    if sys.argv[i].isdigit():
      p[co - argfirstport] = int(sys.argv[i])
      co += 1
      actualports = co - argfirstport
    i += 1

  signal.signal(signal.SIGTERM, service_shutdown)
  signal.signal(signal.SIGINT, service_shutdown)
  sr[0] = server.Server()
  sr[0].start()

  for i in range(actualports):
    try:
      ss[i] = serversocket.ServerSocket(host, p[i])
      ss[i].start()
      time.sleep(2)

    except ServiceExit:
      #sr[i].sflg.set()
      ss[i].sflg.set()
      ss[i].join()
      ss[i].close()
  sr[0].join()

if __name__ == '__main__':
  main(sys.argv[1:])
