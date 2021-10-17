#!/usr/bin/env python3

# Tests
import ssl
import time
import test
import signal
import socket
import struct
import unittest
import threading

import db
import worker
import helper
import client
import server
import serversocket

class TestSmurfer(unittest.TestCase):
  def test_client_server(self):
    """
    Test that the client can connect to the server
    """
    s1 = server.Server()
    s2 = serversocket.ServerSocket("127.0.0.1", 12345, 1)
    c = client.Client("127.0.0.1", 12345, 1)
    s1.start()
    s2.start()
    time.sleep(0.5)
    c.start()
    s1.sflg.set()
    s2.sflg.set()
    c.join()
    s1.join()
    s2.join()
    s2.close()

  def test_many(self):
    """
    Test that the client can connect to several server ports.
    This test is abit flakey, rerun if you get connection refused.
    need more sleep somewhere?
    """
    i = 0
    ports = [5000,5001,5002,5003,5004]
    s = server.Server()
    srv = [None]*10
    cli = [None]*10
    time.sleep(0.5)
    s.start()
    for port in ports:
      srv[i] = serversocket.ServerSocket("127.0.0.1", port, 1)
      cli[i] = client.Client("127.0.0.1", port, 1)
      srv[i].start()
      time.sleep(1)
      cli[i].start()
      srv[i].sflg.set()
      cli[i].join()
      srv[i].join()
      srv[i].close()
      i += 1
    s.sflg.set()
    s.join()

  def test_sanity(self):
    """
    Test sanity
    """
    result = 3
    self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()
