#!/usr/bin/env python3

# Tests
import ssl
import time
import test
import signal
import socket
import struct
import threading

import worker
import helper
import db

import unittest
import srv

class TestSmurfer(unittest.TestCase):

  def test_server(self):
    """
    Test that the server can start
    """
    s1 = srv.Server()
    s2 = srv.ServerSocket("127.0.0.1", 12345, 1)

    s1.start()
    s2.start()
    time.sleep(0.5)
    s1.shutdown_flag.set()
    s2.shutdown_flag.set()
    s1.join()
    s2.join()
    s2.close()

  def test_sanity(self):
    """
    Test sanity
    """
    result = 3
    self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()
