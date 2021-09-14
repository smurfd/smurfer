#!/usr/bin/env python3

# Client
import ssl
import time
import socket
import worker
import helper

w = worker.worker()

def c():
  time.sleep(10)
  print("yayayayya wurkin!!!")
 
def Main():
  host = '127.0.0.1'
  port = 12345
  helper.crtchk()
  sc = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='selfsigned.cert')

  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.connect((host,port))
  job = "1"
  message = "all work and no play makes smurf a smurfy smurf"
  while True:
    if w.get_jobstatus() == w.nojob:
      print("no work")
      w.set_jobstatus(w.hasjob)
      w.dowork(c)

    elif w.get_jobstatus() == w.hasjob:
      print("work")
      x = w.receive_job()
      x()
      break
    s.send(job.encode('ascii'))
    s.send(message.encode('ascii')) # Send to server
    data = s.recv(1024) # Rcv from server
    #break;
  s.close()

if __name__ == '__main__':
    Main()