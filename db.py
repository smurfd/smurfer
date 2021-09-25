#!/usr/bin/env python3

# DB
import os
import sqlite3
import threading

class Database(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def init_srv(self):
    connection = sqlite3.connect("srv.db")
    cursor = connection.cursor()
    if os.path.getsize('srv.db') == 0: # Check if this is a newly created db
      cursor.execute("CREATE TABLE workers (id INTEGER PRIMARY KEY AUTOINCREMENT, job INTEGER, usr STRING)")
    return cursor

  def init_cli(self):
    connection = sqlite3.connect("cli.db")
    cursor = connection.cursor()
    if os.path.getsize('cli.db') == 0: # Check if this is a newly created db
      cursor.execute("CREATE TABLE workers (id INTEGER, usr STRING)")
    return cursor

  def insert(self,c, id, job, usr):
    c.execute("INSERT INTO workers VALUES (?, ?, ?)", (id, job, usr))

  def getjob(self,c, id, usr):
    return c.execute("SELECT job FROM workers WHERE id=? and usr=?",(id,usr),).fetchall()

  def getnextid(self,c):
    return max(max(c.execute("SELECT MAX(id) FROM workers").fetchall())) + 1

  def setjob(self,c, id, job, usr):
    c.execute("UPDATE workers SET job = ? WHERE id = ? and usr=?",(job, id, usr))
