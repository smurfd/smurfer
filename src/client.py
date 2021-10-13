import ssl
import time
import socket
import struct
import threading

import worker
import helper

class Client(threading.Thread):
  def __init__(self, host, port, test=0):
    threading.Thread.__init__(self)
    self.w = worker.worker()
    self.shutdown_flag = threading.Event()
    self.host = host
    self.port = port
    self.job = "1"
    self.help = helper.Helper()
    self.biggerdata = b''
    self.test = test
    self.s = None
    self.ss = None

  def run(self):
    self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.ss = ssl.wrap_socket(self.s,ca_certs="lib/selfsigned.cert",cert_reqs=ssl.CERT_REQUIRED)

  def sending(self):
    self.ss.connect((self.host, self.port))
    if self.test == 0:
      self.help.crtchk_cli()
      self.exchange_cert()
      self.exchange_data()

  def exchange_cert(self):
    c, n, t = self.help.cli_enc()
    self.cli_send_n_t(n, t, c)

  def exchange_data(self):
    message = "all work and no play makes smurf a smurfy smurf"
    while not self.shutdown_flag.is_set():
      time.sleep(0.5)
      if self.w.get_jobstatus() == self.w.nojob:
        self.w.set_jobstatus(self.w.hasjob)
        self.w.dowork(localjob)
      elif self.w.get_jobstatus() == self.w.hasjob:
        wrk = self.w.receive_job()
        wrk()
        break
      length = struct.pack('>Q', len(self.biggerdata))
      self.ss.send(self.job.encode('ascii'))
      self.ss.send(message.encode('ascii')) # Send to server
      self.ss.sendall(length)
      self.ss.sendall(self.biggerdata)
      data = self.ss.recv(1024) # Rcv from server
      ack = self.ss.recv(1)
      assert len(ack) == 1

  def setbigdata(self, bd):
    self.biggerdata = bd

  def cli_send_n_t(self, nonce, tag, c):
    length = struct.pack('>Q', len(nonce))

    self.ss.send(c.nonce)
    self.ss.send(tag)
    self.ss.send(length)
    self.ss.send(nonce)

def localjob():
  time.sleep(1)