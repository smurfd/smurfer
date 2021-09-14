#!/usr/bin/env python3

# Server
from _thread import *
import ssl
import time
import threading
import socket  
import worker 

print_lock = threading.Lock()
w = worker.worker()

def wrk():
  time.sleep(6)
  print("wurkin frum srv")

def sndjob():
  print("Sending new job to client")
  w.send_job(wrk)

def recvdata():
  print("Receiving clients data from job")
  w.receive_data()

def threaded(c):
  while True:
    # data received from client
    typ = c.recv(1)
    data = c.recv(1024)
    if not data: # Close worker connection
      print_lock.release()
      break
    if typ == b'1': # Worker has finished his job
      recvdata()
      sndjob()
    if typ == b'0': # Worker needs work
      sndjob()
    c.send(data)
  c.close()
  
def Main():
  host = "127.0.0.1"
  port = 12345

  sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  sc.load_cert_chain('selfsigned.cert', 'selfsigned.key')
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(5)
  while True:
    c, addr = s.accept()
    print_lock.acquire()
    start_new_thread(threaded, (c,))
  s.close()
 
if __name__ == '__main__':
  Main()