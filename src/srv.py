#!/usr/bin/env python3

# Server
import ssl
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

def main():
  signal.signal(signal.SIGTERM, service_shutdown)
  signal.signal(signal.SIGINT, service_shutdown)

  try:
    s1 = server.Server()
    s2 = serversocket.ServerSocket("127.0.0.1", 12345)

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
  main()
