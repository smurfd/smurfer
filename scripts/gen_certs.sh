#!/bin/sh
openssl req -x509 -newkey rsa:2048 -keyout lib/selfsigned.key -nodes -out lib/selfsigned.cert -sha256 -days 1000
openssl rsa -in lib/selfsigned.key -pubout > lib/selfsigned.pub
