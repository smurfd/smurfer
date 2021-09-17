#!/usr/bin/env python3

# DB
import os
import sqlite3

def init_srv():
  connection = sqlite3.connect("srv.db")
  cursor = connection.cursor()
  if os.path.exists('srv.db') == False:
    cursor.execute("CREATE TABLE workers (id INTEGER PRIMARY KEY AUTOINCREMENT, job INTEGER, usr STRING)")
  return cursor

def init_cli():
  connection = sqlite3.connect("cli.db")
  cursor = connection.cursor()
  if os.path.exists('cli.db') == False:
    cursor.execute("CREATE TABLE workers (id INTEGER, usr STRING)")
  return cursor

def insert(c, id, job, usr):
  c.execute("INSERT INTO workers VALUES (?, ?, ?)", (id, job, usr))

def getjob(c, id, usr):
  return c.execute("SELECT job FROM workers WHERE id=? and usr=?",(id,usr),).fetchall()

def getnextid(c):
  return max(max(c.execute("SELECT MAX(id) FROM workers").fetchall())) + 1

def setjob(c, id, job, usr):
  c.execute("UPDATE workers SET job = ? WHERE id = ? and usr=?",(job, id, usr))