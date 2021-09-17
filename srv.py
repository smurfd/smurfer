#!/usr/bin/env python3

# Server
import ssl
import time
import threading
import socket

import worker
import helper
import db

def wrk():
  time.sleep(6)

def sndjob(w):
  w.send_job(wrk)

def recvdata(w):
  w.receive_data()

def threaded(c, lck, w):
  while True:
    typ = c.recv(1) # data received from client
    data = c.recv(1024)
    if not data: # Close worker connection
      lck.release()
      break
    if typ == b'1': # Worker has finished his job
      recvdata(w)
      sndjob(w)
    if typ == b'0': # Worker needs work
      sndjob(w)
    c.send(data)
  c.close()

def srv_init(host,port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(5)
  return s

def srv_close(s,sc):
  cs.shutdown(socket.SHUT_RDWR)
  cs.close()
  s.close()

def Main():
  pl = threading.Lock()
  w = worker.worker()
  s = srv_init("127.0.0.1", 12345)
  helper.crtchk()
  d = db.init_srv()
  db.insert(d, 1, 1, "smurf")
  #print(db.getjob(d, 1, "smurf"))
  db.insert(d, 2, 0, "smurf1")
  jobid = db.getjob(d, 1, "smurf")
  usrid = db.getnextid(d)


  while True:
    newsocket, fromaddr = s.accept()
    cs = ssl.wrap_socket(newsocket,server_side=True,certfile="selfsigned.cert",keyfile="selfsigned.key")
    pl.acquire()
    threading.Thread(target=threaded, args=(cs,pl,w,)).start()
  srv_close(s,sc)

if __name__ == '__main__':
  Main()