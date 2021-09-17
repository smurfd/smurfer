#!/usr/bin/env python3

# Userdefined Worker class
# the idea was to be able to have worker.py be never touched.
# then what you want to do you add in worker_userdef.py
import os

class worker_userdef():
  hasjob="1"
  nojob="0"
  jobstatus="0"
  workerid="0"
  def job(self):
    pass

  def send_job(self,w):
    self.job = w()

  def receive_job(self):
    return self.job
 
  def receive_data(self):
    pass
 
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

def method():
  pass