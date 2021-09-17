# smurfer
Need some smurfing done? smurfer smurfs
Idea is to create a general worker that distributes the working between server and client, and you can define what you want it todo.

# install
install pyenv and virtualenv via package manager:
`brew install pyenv virtualenv`
`apt install pyenv virtualenv`
`zypper in pyenv virtualenv`
`dnf install pyenv virtualenv`
`emerge -vaD pyenv virtualenv`
Or grab pyenv manually:
```
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
$ echo "export PATH=\"${PYENV_ROOT}/bin:\$PATH\"" >> ~/.zshrc
$ echo "eval \"\$(pyenv init -)\"" >> ~/.zshrc
$ echo "eval \"\$(pyenv virtualenv-init -)\"" >> ~/.zshrc
```

```
$ pyenv install 3.8.12 (3.6.x and 3.7.x not supported on Mac m1)

$ git clone https://github.com/smurfd/smurfer
$ cd smurfer
$ pyenv local 3.8.12
$ virtualenv -p $HOME/.pyenv/versions/3.8.12/bin/python3 venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```
in one terminal, run :
$ python3 srv.py

in another terminal run :
$ python3 cli.py

# srv
- wait for connection from client
- if client has no job, provide new job
- if client has finished job, receive result and provide new job

# cli
- connect to server
- receive job
- disconnect from server
- do work
- connect to server
- provide result
- receive new job
- disconnect from server

# TODO
- Set pid per worker
- Send more data
- pools of server ips/ports to listen on
