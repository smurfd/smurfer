#!/usr/bin/env python3

# Worker class
import os.path
from os import path

class worker_userdef:
  hasjob="1"
  nojob="0"
  jobstatus="0"
  workerid="0"
  def job(self):
    pass

  def send_job(self,w):
    print("userdef sending job")
    self.job = w()

  def receive_job(self):
    print("userdef receiving job")
    return self.job
 
  def receive_data(self):
    print("userdef receiving data")
 
  def set_jobstatus(self,j):
    self.jobstatus = j

  def get_jobstatus(self):
    return self.jobstatus

  def set_clientid(self,i):
    self.clientid = i

  def get_clientid(self):
    return self.clientid

  def dowork(self,w):
    w()
    print("userdef wrk done")

def method():
  print("userdef wurker...")
