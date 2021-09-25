#!/usr/bin/env python3

# Server
import ssl
import time
import threading
import signal
import socket

import worker
import helper
import db

class Server(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.shutdown_flag = threading.Event()
    self.db = db.Database()
    self.help = helper.Helper()

  def run(self):
    self.help.crtchk()
    d = self.db.init_srv()
    self.db.insert(d, 1, 1, "smurf")
    self.db.insert(d, 2, 0, "smurf1")
    jobid = self.db.getjob(d, 1, "smurf")
    usrid = self.db.getnextid(d)

    while not self.shutdown_flag.is_set():
      time.sleep(0.5)
 
class ServerSocket(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.shutdown_flag = threading.Event()

  def run(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.settimeout(10)
    s.bind(("127.0.0.1", 12345))
    s.listen(5)

    w = worker.worker()
    while not self.shutdown_flag.is_set():
      try:
        newsocket, fromaddr = s.accept()
        self.cs = ssl.wrap_socket(newsocket,server_side=True,certfile="selfsigned.cert",keyfile="selfsigned.key")
        typ = self.cs.recv(1) # data received from client
        data = self.cs.recv(1024)
        if not data:
          break
        if typ == b'1': # Worker has finished his work
          recvdata(w)
          sndjob(w)
        if typ == b'0': # Worker needs work
          sndjob(w)
        self.cs.send(data)
      except IOError as e: # Handle BlockingIOError
        pass
    time.sleep(0.5)

class ServiceExit(Exception):
  pass

def service_shutdown(signum, frame):
  raise ServiceExit

def wrk():
  time.sleep(6)

def sndjob(w):
  w.send_job(wrk)

def recvdata(w):
  w.receive_data()

def main():
  signal.signal(signal.SIGTERM, service_shutdown)
  signal.signal(signal.SIGINT, service_shutdown)

  try:
    s1 = Server()
    s2 = ServerSocket()

    s1.start()
    s2.start()

    while True:
      time.sleep(0.5)

  except ServiceExit:
    s1.shutdown_flag.set()
    s2.shutdown_flag.set()
    s1.join()
    s2.join()
 
if __name__ == '__main__':
  main()
