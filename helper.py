#!/usr/bin/env python3

# Helper
import os
import ctypes
import threading

class Helper(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

# Check if a selfsigned certificate and key exist, if not print how to create them.
  def crtchk(self):
    if not os.path.isfile('selfsigned.cert'):
      print("Create a selfsigned cert & key using this command :")
      print("$ openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000")
      print("use 'localhost' as Common Name")
      quit()
    if not os.path.isfile('selfsigned.key'):
      print("Create a selfsigned cert & key using this command :")
      print("$ openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000")
      print("use 'localhost' as Common Name")
      quit()

  def call_cworker(self):
    if not os.path.isfile('./libcworker.so'):
      print("libcworker.so does not exist. Compile it using this command :")
      print("gcc -shared -o libcworker.so -fPIC cworker.c")
      quit()
    libcwrk = ctypes.CDLL('./libcworker.so')
    print("doing work", libcwrk.dowork(100))
