#!/usr/bin/env python3

# Client
import ssl
import time
import socket
import struct
import threading

import worker
import helper
import client

def main():
  c = client.Client("127.0.0.1",12345)
  c.setbigdata(b'D4T4B1GggR&B1gGgggR!'*10000)
  c.start()
  time.sleep(2)
  c.sending()
  c.help.call_cworker()

  c.join()

if __name__ == '__main__':
    main()
