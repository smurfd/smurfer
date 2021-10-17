import ssl
import time
import socket
import struct
import threading

import worker
import helper

class Client(threading.Thread):
  def __init__(self, host, port, test=0):
    threading.Thread.__init__(self, group=None)
    self.jobs = "1"
    self.host = host
    self.port = port
    self.test = test
    self.sock = None
    self.ssls = None
    self.conn = None
    self.addr = None
    self.biggerdata = b''
    self.work = worker.worker()
    self.sflg = threading.Event()
    self.help = helper.Helper()

  def run(self):
    self.help.crtchk_cli()
    self.connect()
    self.exchange_cert()
    self.send()

  def connect(self):
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.ssls = ssl.wrap_socket(self.sock, ca_certs="lib/selfsigned.cert", cert_reqs=ssl.CERT_REQUIRED)
    self.ssls.connect((self.host, self.port))

  def send_cert(self, nonce, tag, c):
    length = struct.pack('>Q', len(nonce))
    self.ssls.send(c.nonce)
    self.ssls.send(tag)
    self.ssls.send(length)
    self.ssls.send(nonce)

  def exchange_cert(self):
    c, n, t = self.help.cli_enc()
    self.send_cert(n, t, c)

  def send(self):
    time.sleep(0.5)
    self.handle_workstate()
    self.send_data()

  def send_data(self):
    length = struct.pack('>Q', len(self.biggerdata))
    self.ssls.send(self.jobs.encode('ascii'))
    time.sleep(0.5)
    self.ssls.sendall(length)
    self.ssls.sendall(self.biggerdata)
    #data = self.ssls.recv(1024) # Rcv from server
    ack = self.ssls.recv(1)
    assert len(ack) == 1

  def handle_workstate(self):
    while not self.sflg.is_set():
      if self.work.get_jobstatus() == self.work.nojob:
        self.work.set_jobstatus(self.work.hasjob)
        self.work.dowork(localjob)
      elif self.work.get_jobstatus() == self.work.hasjob:
        wrk = self.work.receive_job()
        wrk()
        break

  def setbigdata(self, bd):
    self.biggerdata = bd

def localjob():
  time.sleep(1)
