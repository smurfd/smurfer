#!/usr/bin/env python3

# Helper
import os
import ctypes
import threading

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

class Helper(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  # Check if a selfsigned certificate and key exist, if not print how to create them.
  def crtchk(self):
    if not os.path.isfile('selfsigned.cert'):
      print("Create a selfsigned cert & key using this command :")
      print("$ openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000")
      print("$ openssl rsa -in selfsigned.key -pubout > selfsigned.pub")
      print("use 'localhost' as Common Name")
      quit()
    if not os.path.isfile('selfsigned.key'):
      print("Create a selfsigned cert & key using this command :")
      print("$ openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000")
      print("$ openssl rsa -in selfsigned.key -pubout > selfsigned.pub")
      print("use 'localhost' as Common Name")
      quit()

  def call_cworker(self):
    if not os.path.isfile('./libcworker.so'):
      print("libcworker.so does not exist. Compile it using this command :")
      print("$ gcc -shared -o libcworker.so -fPIC cworker.c")
      quit()
    libcwrk = ctypes.CDLL('./libcworker.so')
    print("doing work", libcwrk.dowork(100))

  def enc(key, data):
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher, ciphertext, tag

  def dec(key, nonce, tag, data):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
      cv =  cipher.decrypt_and_verify(data, tag)
      return cv
    except ValueError as e:
      print(e)
      return None

#k = os.urandom(32)
#dd = b'awholelotsofdata'*100000
#cc, c,t = enc1(k, dd)
#pt = dec1(k, cc.nonce, t, c)