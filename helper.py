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
  def crtchk_srv(self):
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

  def crtchk_cli(self):
    if not os.path.isfile('selfsigned.pub'):
      print("You need the public key. Get it by :")
      print("$ curl https://smurfd.serveblog.net/selfsigned.pub --output selfsigned.pub")
      print("its not there yet... ")
      quit()

  def call_cworker(self):
    if not os.path.isfile('./libcworker.so'):
      print("libcworker.so does not exist. Compile it using this command :")
      print("$ gcc -shared -o libcworker.so -fPIC cworker.c")
      quit()
    libcwrk = ctypes.CDLL('./libcworker.so')
    print("doing work", libcwrk.dowork(100))

  def enc(self, key, data):
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher, ciphertext, tag

  def dec(self, key, nonce, tag, data):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
      cv =  cipher.decrypt_and_verify(data, tag)
      return cv
    except ValueError as e:
      print(e)
      return None

  def cli_enc(self):
    key = RSA.importKey(open('selfsigned.pub').read()) # public
    k = key.exportKey()
    k_rand = k[27:59] # skip this part : -----BEGIN PUBLIC KEY-----
    dd = b'awholelotsofdata'*100000
    cc,c,t = enc(k_rand, dd) # encrypt on cli using part of pub key
    return cc, t

  def srv_dec(self, nonce, tag):
    pri_key = RSA.importKey(open('selfsigned.key').read()) # private
    k = pri_key.publickey().exportKey('PEM')
    k_rand = k[27:59] # skip this part : -----BEGIN PUBLIC KEY-----
    dd = b'awholelotsofdata'*100000
    pt = dec(k_rand, nonce, tag, c) # decrypt on srv using pub key from priv key
    return pt

