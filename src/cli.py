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
  if (len(sys.argv) < 3) or (len(sys.argv) > 3):
    print("Usage: ./src/cli.py <host> <port>")
    sys.exit(2)
  host = sys.argv[1]
  port = int(sys.argv[2])
  try:
    c = client.Client(host, port)
    c.setbigdata(b'D4T4B1GggR&B1gGgggR!'*10000)
    c.start()
    time.sleep(2)
    c.sending()
    c.help.call_cworker()
    c.join()
  except Exception:
    print("Could not connec to Server @ ", host, ":", port)

if __name__ == '__main__':
    main(sys.argv[1:])
