# smurfer
Need some smurfing done? smurfer smurfs
Idea is to create a general worker that distributes the working between server and client, and you can define what you want it todo.

=== install
install pyenv and virtualenv via package manager:
brew install pyenv; apt install pyenv; zypper in pyenv; dnf install pyenv; emerge -vaD pyenv
$ pyenv install 3.8.12 (3.6.x and 3.7.x not supported on Mac m1)

$ git clone https://github.com/smurfd/smurfer
$ cd smurfer
$ pyenv local 3.8.12
$ virtualenv -p $HOME/.pyenv/versions/3.8.12/bin/python3 venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt

in one terminal, run :
$ python3 srv.py

in another terminal run :
$ python3 cli.py

=== srv
wait for connection from client
if client has no job, provide new job
if client has finished job, receive result and provide new job

=== cli
connect to server
receive job
disconnect from server
do work
connect to server
provide result
receive new job
disconnect from server


=== TODO
- need more ssl?
- asyncio instead?
- Call clib if like libworker.so is available
- Set pid per worker
- Send more data
- pools of server ips/ports to listen on
