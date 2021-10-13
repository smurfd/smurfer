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
  if (len(sys.argv) < 3) or (len(sys.argv) > 3):
    print("Usage: ./src/srv.py <host> <port>")
    sys.exit(2)
  host = sys.argv[1]
  port = int(sys.argv[2])
  signal.signal(signal.SIGTERM, service_shutdown)
  signal.signal(signal.SIGINT, service_shutdown)

  try:
    s1 = server.Server()
    s2 = serversocket.ServerSocket(host, port)

    s1.start()
    s2.start()
    time.sleep(2)
    s2.receiving()
    while True:
      time.sleep(0.5)

  except ServiceExit:
    s1.shutdown_flag.set()
    s2.shutdown_flag.set()
    s1.join()
    s2.join()
 
if __name__ == '__main__':
  main(sys.argv[1:])
