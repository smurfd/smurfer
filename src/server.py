import ssl
import time
import signal
import socket
import struct
import threading

import worker
import helper
import db

class Server(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.sflg = threading.Event()
    self.db = db.Database()
    self.help = helper.Helper()

  def run(self):
    self.help.crtchk_srv()
    d = self.db.init_srv()
    self.db.insert(d, 1, 1, "smurf")
    self.db.insert(d, 2, 0, "smurf1")
    jobid = self.db.getjob(d, 1, "smurf")
    usrid = self.db.getnextid(d)

    while not self.sflg.is_set():
      time.sleep(0.5)
