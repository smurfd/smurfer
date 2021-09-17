#!/usr/bin/env python3

# Client
import ssl
import time
import socket

import worker
import helper

def localjob():
  time.sleep(10)

def cli_init(host,port):
  helper.crtchk()
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  ss = ssl.wrap_socket(s,ca_certs="selfsigned.cert",cert_reqs=ssl.CERT_REQUIRED)
  ss.connect((host,port))
  return s, ss

def cli_close(s, ss):
  ss.close()
  s.close()

def Main():
  w = worker.worker()
  s,ss = cli_init("127.0.0.1", 12345)
  job = "1"
  message = "all work and no play makes smurf a smurfy smurf"
  while True:
    if w.get_jobstatus() == w.nojob:
      w.set_jobstatus(w.hasjob)
      w.dowork(localjob)
    elif w.get_jobstatus() == w.hasjob:
      wrk = w.receive_job()
      wrk()
      break
    ss.send(job.encode('ascii'))
    ss.send(message.encode('ascii')) # Send to server
    data = ss.recv(1024) # Rcv from server
  cli_close(s,ss)
  helper.call_cworker()

if __name__ == '__main__':
    Main()