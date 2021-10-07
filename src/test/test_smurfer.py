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

  def test_server(self):
    """
    Test that the server can start
    """
    s1 = server.Server()
    s2 = serversocket.ServerSocket("127.0.0.1", 12345, 1)

    s1.start()
    s2.start()
    time.sleep(0.5)
    s1.shutdown_flag.set()
    s2.shutdown_flag.set()
    s1.join()
    s2.join()
    s2.close()

  def test_client(self):
    """
    Test that the client can connect to the server
    """
    s1 = server.Server()
    s2 = serversocket.ServerSocket("127.0.0.1", 12345, 1)
    c = client.Client("127.0.0.1", 12345, 1)
    s1.start()
    s2.start()
    time.sleep(2)
    c.start()

    s1.shutdown_flag.set()
    s2.shutdown_flag.set()
    s1.join()
    s2.join()
    s2.close()
    #c.join()

  def test_sanity(self):
    """
    Test sanity
    """
    result = 3
    self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()
