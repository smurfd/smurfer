import ssl
import time
import signal
import socket
import struct
import threading

import worker
import helper
import db

class ServerSocket(threading.Thread):
  def __init__(self, host, port, test=0):
    threading.Thread.__init__(self)
    self.shutdown_flag = threading.Event()
    self.host = host
    self.port = port
    self.test = test
    self.s = None
    self.ss = None
    self.help = helper.Helper()

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

  def __enter__(self):
    return self

  def close(self):
    self.s.close()

  def run(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.setblocking(0)
    self.s.settimeout(10)
    self.s.bind((self.host, self.port))
    self.s.listen(5)

    w = worker.worker()
    while not self.shutdown_flag.is_set():
      try:
        newsocket, fromaddr = self.s.accept()
        self.ss = ssl.wrap_socket(newsocket,server_side=True,certfile="lib/selfsigned.cert",keyfile="lib/selfsigned.key")
        n, t, c = self.recv_n_t()
        self.help.srv_dec(n, t, c)
        typ = self.ss.recv(1) # data received from client
        data = self.ss.recv(1024)
        if not data:
          break
        if typ == b'1': # Worker has finished his work
          recvdata(w)
          sndjob(w)
        if typ == b'0': # Worker needs work
          sndjob(w)
        self.ss.send(data)
        recvlen = self.ss.recv(8) # Receive length of data
        (length,) = struct.unpack('>Q', recvlen)
        bigdata = b''
        while len(bigdata) < length:
          to_read = length - len(bigdata)
          bigdata += self.ss.recv(4096 if to_read > 4096 else to_read)
          self.ss.sendall(b'\00') # Send 0 ack = OK
        if self.test == 1:
          break
      except IOError as e: # Handle BlockingIOError by ignoring
        pass
    time.sleep(0.5)

  def recv_n_t(self):
    n = self.ss.recv(1024)
    t = self.ss.recv(1024)
    recvlen = self.ss.recv(8)
    (length,) = struct.unpack('>Q', recvlen)
    bigdata = b''
    while len(bigdata) < length:
      to_read = length - len(bigdata)
      bigdata += self.ss.recv(4096 if to_read > 4096 else to_read)

    return n, t, bigdata

def wrk():
  time.sleep(6)

def sndjob(w):
  w.send_job(wrk)

def recvdata(w):
  w.receive_data()
