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
    threading.Thread.__init__(self, group=None)
    self.test = test
    self.host = host
    self.port = port
    self.sock = None # Socket
    self.ssls = None # SSL Socket
    self.conn = None
    self.addr = None
    self.help = helper.Helper()
    self.work = worker.worker()
    self.sflg = threading.Event()

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

  def __enter__(self):
    return self

  def close(self):
    self.sock.close()

  def run(self):
    self.listen()
    while not self.sflg.is_set():
      try:
        self.receive()
        self.exchange_cert()
        state = self.receive_workstate()
        data = self.receive_data()
        if not data:
          break
        if self.test == 1:
          break
        self.handle_workstate(state)

      except IOError as e: # Handle BlockingIOError by ignoring
        pass

  def listen(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.host, self.port))
    self.sock.listen(10)

  def receive(self):
    time.sleep(0.5)
    self.conn, self.addr = self.sock.accept()
    self.ssls = ssl.wrap_socket(self.conn, server_side=True, certfile="lib/selfsigned.cert", keyfile="lib/selfsigned.key")

  def receive_cert(self):
    n = self.ssls.recv(1024)
    t = self.ssls.recv(1024)
    recvlen = self.ssls.recv(8)
    (length,) = struct.unpack('>Q', recvlen)
    bigdata = b''
    while len(bigdata) < length:
      to_read = length - len(bigdata)
      bigdata += self.ssls.recv(4096 if to_read > 4096 else to_read)
    return n, t, bigdata

  def exchange_cert(self):
    n, t, c = self.receive_cert()
    self.help.srv_dec(n, t, c)

  def receive_workstate(self):
    state = self.ssls.recv(1) # data received from client
    return state

  def handle_workstate(self, state):
    if state == b'1': # Worker has finished his work
      recvdata(self.work)
      sndjob(self.work)
    if state == b'0': # Worker needs work
      sndjob(self.work)

  def receive_data(self):
    recvlen = self.ssls.recv(8) # Receive length of data
    (length,) = struct.unpack('>Q', recvlen)
    bigdata = b''
    while len(bigdata) < length:
      to_read = length - len(bigdata)
      bigdata += self.ssls.recv(4096 if to_read > 4096 else to_read)
    self.ssls.sendall(b'\00') # Send 0 ack = OK
    return bigdata

def wrk():
  time.sleep(6)

def sndjob(w):
  w.send_job(wrk)

def recvdata(w):
  w.receive_data()
