#!/usr/bin/env python3

# Client
import ssl
import time
import socket
import struct
import threading

import worker
import helper

class Client(threading.Thread):
  def __init__(self, host, port):
    threading.Thread.__init__(self)
    self.w = worker.worker()
    self.shutdown_flag = threading.Event()
    self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.ss = ssl.wrap_socket(self.s,ca_certs="selfsigned.cert",
      cert_reqs=ssl.CERT_REQUIRED)
    self.ss.connect((host, port))
    self.job = "1"
    self.help = helper.Helper()
    self.biggerdata = b''

  def run(self):
    message = "all work and no play makes smurf a smurfy smurf"
    self.help.crtchk_cli()
    n, t = helper.cli_enc()
    cli_send_n_t(n, t)

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

  def cli_send_n_t(self, nonce, tag):
    self.ss.send(nonce)
    self.ss.send(tag)

def localjob():
  time.sleep(1)

def main():
  c = Client("127.0.0.1",12345)
  c.setbigdata(b'D4T4B1GggR&B1gGgggR!'*10000)
  c.start()
  c.help.call_cworker()
  c.join()

if __name__ == '__main__':
    main()
