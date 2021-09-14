import os

def crtchk():
  if not os.path.isfile('selfsigned.cert'):
    print("Create a selfsigned cert & key using this command : openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000")
    print("use 'localhost' as Common Name")
    quit()
  if not os.path.isfile('selfsigned.key'):
    print("Create a selfsigned cert & key using this command : openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000")
    print("use 'localhost' as Common Name")
    quit()
